from noteline.core import noteline_notebook, envs


from kfp.dsl._container_op import ContainerOp


class NotelineNbOp(ContainerOp):

  def __init__(self,
               notebook_in: str,
               notebook_out: str = None,
               op_name: str = None,
               image: str = None,
               **kwargs):
    if not notebook_in:
      raise ValueError("notebook_in can't be empty. Current value: {}".format(
          notebook_in))
    if not notebook_out:
      notebook_out = notebook_in

    noteline_notebook_obj = noteline_notebook.get_noteline_notebook(notebook_in)
    env = noteline_notebook_obj.get_env()
    if env.get("type", "") == envs.DOCKER_ENV_TYPE:
      if image:
        print("looks like both input env ({}) provided and env from"
              " notebook({}). Using env provided explicitly".format(image,
                                                                    str(env)))
      else:
        image = env["uri"]

    if not image:
      image = "gcr.io/deeplearning-platform-release/tf-cpu"

    if image and image in kwargs:
      raise ValueError(
          "image should be set as input variable, and not via kwargs")

    if not op_name:
      op_name = notebook_in.replace("-", "_").replace(".", "_").replace("/",
                                                                        "_")

    if "command" in kwargs:
      raise ValueError("command should NOT be passed in kwargs")
    if "arguments" in kwargs:
      raise ValueError("arguments should NOT be passed in kwargs")

    kwargs["image"] = image
    kwargs["command"] = ["nbexecutor"]
    kwargs["arguments"] = ["--input-notebook", notebook_in,
                           "--output-notebook", notebook_out]

    super().__init__(name=op_name, **kwargs)
