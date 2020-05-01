import nbformat


class NotelineNotebook(object):

  def __init__(self, notebook: nbformat.NotebookNode):
    self.notebook = notebook

  def get_env(self):
    if "env" not in self.notebook.metadata:
        raise ValueError("There is no 'env' key in the Notebook's metadata")
    return self.notebook.metadata.env
