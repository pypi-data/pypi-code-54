import os

class App_Paths:
    path_module_script_path = os.path.abspath(__file__)
    base_script_path = os.path.dirname(os.path.dirname(path_module_script_path))
    base_web_data_dir_path = os.path.join(base_script_path, 'web_data')
    base_firefox_driver_path = os.path.join(base_script_path, 'firefox_driver')
    firefox_driver_path = None

    def __init__(self):
        self.try_set_firefox_driver_path(False)

    def try_set_firefox_driver_path(self, verbose=True):
        if self.firefox_driver_path is None:
            if os.path.isdir(self.base_firefox_driver_path) == False:
                if verbose:
                    print('Firefox driver directory has not yet been created')
                    print(f'Firefox driver directory path: {self.base_firefox_driver_path}')
                return None
            if len(os.listdir(self.base_firefox_driver_path)) == 0:
                if verbose:
                    print('Firefox driver directory is empty. Please download firefox driver')
                    print(f'Firefox driver directory path: {self.base_firefox_driver_path}')
                return None
            self.firefox_driver_path = os.path.join(self.base_firefox_driver_path, os.listdir(self.base_firefox_driver_path)[0], 'geckodriver.exe')
        return self.firefox_driver_path