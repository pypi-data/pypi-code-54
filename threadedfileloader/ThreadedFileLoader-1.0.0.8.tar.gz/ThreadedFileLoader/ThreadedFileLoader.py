from threading import Thread
import imageio
import glob


class ThreadedFileLoader:
    """
    Class to load files via threading.
    Usage:
    =====
    Overload the `self.object_loader` for customized file type.
    """

    def __init__(self, folder_path_glob):
        self.loaded_objects = []
        self.file_paths = self.glob_resolver(folder_path_glob)

    def glob_resolver(self, path_glob):
        return glob.glob(path_glob)

    def object_loader(self, path):
        return imageio.imread(path)

    def loading_function(self, path):
        image = self.object_loader(path)
        self.loaded_objects.append(image)

    def __thread_worker(self):
        for i, file_path in enumerate(self.file_paths):
            Thread(target=self.loading_function(file_path)).start()

    def start_loading(self):
        self.__thread_worker()


class ThreadedImageLoader(ThreadedFileLoader):
    def object_loader(self, path):
        return imageio.imread(path)


class ThreadedTextLoader(ThreadedFileLoader):
    def object_loader(self, path):
        with open(path) as afile:
            return afile.readlines()
