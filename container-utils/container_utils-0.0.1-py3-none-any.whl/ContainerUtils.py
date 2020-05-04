import contextlib, docker, io, json, logging, posixpath, ntpath, os, shutil, sys, tempfile
from .ImageUtils import ImageUtils

class ContainerUtils(object):
	'''
	Provides functionality related to Docker containers
	'''
	
	@staticmethod
	@contextlib.contextmanager
	def automatically_stop(container, timeout=1):
		'''
		Context manager to automatically stop a container returned by `ContainerUtils.start_for_exec()`
		'''
		try:
			yield container
		finally:
			logging.info('Stopping Docker container {}...'.format(container.short_id))
			ContainerUtils.stop(container, timeout=timeout)
	
	@staticmethod
	def container_platform(container):
		'''
		Retrieves the platform identifier for the specified container
		'''
		return container.attrs['Platform']
	
	@staticmethod
	def copy_from_host(container, host_path, container_path):
		'''
		Copies a file or directory from the host system to a container returned by `ContainerUtils.start_for_exec()`.
		
		`host_path` is the absolute path to the file or directory on the host system.
		
		`container_path` is the absolute path to the directory in the container where the copied file(s) will be placed.
		'''
		
		# If the host path denotes a file rather than a directory, copy it to a temporary directory
		# (If the host path is a directory then we create a no-op context manager to use in our `with` statement below)
		tempDir = contextlib.suppress()
		if os.path.isfile(host_path) == True:
			tempDir = tempfile.TemporaryDirectory()
			shutil.copy2(host_path, os.path.join(tempDir.name, os.path.basename(host_path)))
			host_path = tempDir.name
		
		# Automatically delete the temporary directory if we created one
		with tempDir:
			
			# Create a temporary file to hold the .tar archive data
			with tempfile.NamedTemporaryFile(suffix='.tar', delete=False) as tempArchive:
				
				# Add the data from the host system to the temporary archive
				tempArchive.close()
				archiveName = os.path.splitext(tempArchive.name)[0]
				shutil.make_archive(archiveName, 'tar', host_path)
				
				# Copy the data from the temporary archive to the container
				with open(tempArchive.name, 'rb') as archive:
					container.put_archive(container_path, archive.read())
				
				# Remove the temporary archive
				os.unlink(tempArchive.name)
	
	@staticmethod
	def copy_to_host(container, container_path, host_path):
		'''
		Copies a file or directory from a container returned by `ContainerUtils.start_for_exec()` to the host system.
		
		`container_path` is the absolute path to the file or directory in the container.
		
		`host_path` is the absolute path to the directory on the host system where the copied file(s) will be placed.
		'''
		
		# Create a temporary file to hold the .tar archive data
		with tempfile.NamedTemporaryFile(suffix='.tar', delete=False) as tempArchive:
			
			# Copy the data from the container to the temporary archive
			chunks, stat = container.get_archive(container_path)
			for chunk in chunks:
				tempArchive.write(chunk)
			
			# Extract the file to the host system destination
			tempArchive.close()
			shutil.unpack_archive(tempArchive.name, host_path)
			os.unlink(tempArchive.name)
	
	@staticmethod
	def exec(container, command, capture=False, **kwargs):
		'''
		Executes a command in a container returned by `ContainerUtils.start_for_exec()` and streams or captures the output
		'''
		
		# Determine if we are capturing the output or printing it
		stdoutDest = io.StringIO() if capture == True else sys.stdout
		stderrDest = io.StringIO() if capture == True else sys.stderr
		
		# Attempt to start the command
		details = container.client.api.exec_create(container.id, command, **kwargs)
		output = container.client.api.exec_start(details['Id'], stream=True, demux=True)
		
		# Stream the output
		for chunk in output:
			
			# Isolate the stdout and stderr chunks
			stdout, stderr = chunk
			
			# Capture/print the stderr data if we have any
			if stderr is not None:
				print(stderr.decode('utf-8'), end='', flush=True, file=stderrDest)
			
			# Capture/print the stdout data if we have any
			if stdout is not None:
				print(stdout.decode('utf-8'), end='', flush=True, file=stdoutDest)
		
		# Determine if the command succeeded
		capturedOutput = (stdoutDest.getvalue(), stderrDest.getvalue()) if capture == True else None
		result = container.client.api.exec_inspect(details['Id'])['ExitCode']
		if result != 0:
			container.stop()
			raise RuntimeError('Failed to run command {} in container. Process returned exit code {} with output {}.'.format(
				command,
				result,
				capturedOutput if capture == True else 'printed above'
			))
		
		# If we captured the output then return it
		return capturedOutput
	
	@staticmethod
	def exec_multiple(container, commands=[], capture=False, pre_hook=None, post_hook=None, **kwargs):
		'''
		Executes multiple commands in a container returned by `ContainerUtils.start_for_exec()` and streams the output
		'''
		
		# If no pre-execution and post-execution hooks were provided, set them to no-ops
		pre_hook = pre_hook if pre_hook is not None else lambda cmd: None
		post_hook = post_hook if post_hook is not None else lambda cmd: None
		
		# Execute each of our commands, executing the hooks as appropriate
		output = []
		for command in commands:
			pre_hook(command)
			output.append(ContainerUtils.exec(container, command, capture, **kwargs))
			post_hook(command)
		
		# If we captured the output then return it
		return output if capture == True else None
	
	@staticmethod
	def glob(container, pattern):
		'''
		Performs globbing using Python inside a container to list the files matching the specified pattern
		'''
		platform = ContainerUtils.container_platform(container)
		interpreter = 'python' if platform == 'windows' else 'python3'
		command = [interpreter, '-c', 'import glob; print("\\n".join(glob.glob({})))'.format(json.dumps(pattern))]
		stdout, stderr = ContainerUtils.exec(container, command, capture=True)
		return stdout.strip().splitlines()
	
	@staticmethod
	def path(container):
		'''
		Returns the appropriate path module for the platform of the specified container
		'''
		platform = ContainerUtils.container_platform(container)
		return ntpath if platform == 'windows' else posixpath
	
	@staticmethod
	def start_for_exec(client, image, **kwargs):
		'''
		Starts a container in a detached state using a command that will block indefinitely
		and returns the container handle. The handle can then be used to execute commands
		inside the container. The container will be removed automatically when it is stopped,
		but it will need to be stopped manually by calling `ContainerUtils.stop()`.
		'''
		platform = ImageUtils.image_platform(client, image)
		command = ['timeout', '/t', '99999', '/nobreak'] if platform == 'windows' else ['bash', '-c', 'sleep infinity']
		return client.containers.run(
			image,
			command,
			stdin_open = platform == 'windows',
			tty = platform == 'windows',
			detach = True,
			remove = True,
			**kwargs
		)
	
	@staticmethod
	def stop(container, timeout=1):
		'''
		Stops a container returned by `ContainerUtils.start_for_exec()`
		'''
		container.stop(timeout=timeout)
	
	@staticmethod
	def workspace_dir(container):
		'''
		Returns a platform-appropriate workspace path for a container returned by `ContainerUtils.start_for_exec()`
		'''
		platform = ContainerUtils.container_platform(container)
		return 'C:\\workspace' if platform == 'windows' else '/tmp/workspace'
	
	@staticmethod
	def shell_prefix(container):
		'''
		Returns a platform-appropriate command prefix for invoking a shell in a container returned by `ContainerUtils.start_for_exec()`
		'''
		platform = ContainerUtils.container_platform(container)
		return ['cmd', '/S', '/C'] if platform == 'windows' else ['bash', '-c']
