import nbformat

from smart_open import open


class NotelineNotebook(object):

  def __init__(self, notebook: nbformat.NotebookNode):
    self.notebook = notebook

  def get_env(self):
    if "env" not in self.notebook.metadata:
        return {}
    return self.notebook.metadata.env

  def set_env(self,
              name: str = None,
              type: str = None,
              uri: str = None):
    if "env" not in self.notebook.metadata:
      self.notebook.metadata.env = {}

    env = self.notebook.metadata.env
    if name:
      env["name"] = name
    if type:
      env["type"] = type
    if uri:
      env["uri"] = uri

  def save_notebook(self, path: str):
    if not path:
      raise ValueError("notebook path need to be provided. Current value: {}".
                       format(path))
    with open(path, "w") as nb_file:
      nbformat.write(self.notebook, nb_file)


def get_noteline_notebook(notebook_uri: str):
  with open(notebook_uri, "r") as nb_file:
    notebook_obj = nbformat.read(nb_file, nbformat.NO_CONVERT)
  return NotelineNotebook(notebook_obj)
