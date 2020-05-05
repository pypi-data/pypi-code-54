from threading import Thread
import imageio
import glob


class ThreadedFileLoader:
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


# fl = ThreadedFileLoader("t:/coding/2020/may/face_detect/run2020/*.jpg")
# fl.start_loading()
# exit()

# fl = ThreadedImageLoader("t:/coding/2020/may/face_detect/run2020/*.jpg")
# fl.start_loading()
# print(fl.loaded_objects[0][20][20])
# print(len(fl.loaded_objects))
