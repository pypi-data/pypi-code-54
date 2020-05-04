import docker, fnmatch

class ImageUtils(object):
	'''
	Provides functionality related to Docker container images
	'''
	
	@staticmethod
	def build_image(client, **kwargs):
		'''
		Builds a container image, printing progress output as it is received
		'''
		
		# Initiate the build and retrieve the generator for our build events
		events = client.api.build(decode=True, **kwargs)
		imageID = None
		
		# Handle each build event as it is returned by the Docker daemon
		for event in events:
			
			# Determine the event type
			output = event.get('stream', event.get('status', '')).strip()
			details = event.get('progress', '').strip()
			if output != '':
				
				# Progress output
				print('{}{}'.format(output, ' ' + details if details != '' else ''), flush=True)
				
			elif output == '' and len(event.get('stream', '')) > 0:
				
				# Whitespace-only progress output
				pass
				
			elif 'error' in event:
				
				# An error has occurred
				raise RuntimeError('Docker build failed with error: {}'.format(event['error']))
				
			elif 'aux' in event and 'ID' in event['aux']:
				
				# Build succeeded and Docker has returned the image ID
				imageID = event['aux']['ID']
				
			else:
				
				# Unrecognised event type
				print(event, flush=True)
		
		return imageID
	
	@staticmethod
	def image_platform(client, image):
		'''
		Retrieves the platform identifier for the specified image
		'''
		return ImageUtils.list_images(client, image)[0].attrs['Os']
	
	@staticmethod
	def list_images(client, tagFilter = None, filters = {}):
		'''
		Retrieves the details for each image matching the specified filters
		'''
		
		# Retrieve the list of images matching the specified filters
		images = client.images.list(filters=filters)
		
		# Apply our tag filter if one was specified
		if tagFilter is not None:
			images = [i for i in images if len(i.tags) > 0 and len(fnmatch.filter(i.tags, tagFilter)) > 0]
		
		return images
