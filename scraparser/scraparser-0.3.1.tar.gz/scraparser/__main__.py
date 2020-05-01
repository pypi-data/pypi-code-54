import os.path, sys

if __name__ == "__main__":

    if __package__ == "":
        # if the package is run directly with the folder, add
        # the parent folder as part of PYTHONPATH for the
        # current execution environment so the uninstalled
        # "scraparser" package is discoverable.
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

    from .cli import entry_point
    #  pylint: disable=no-value-for-parameter,unexpected-keyword-arg
    entry_point(obj={})
