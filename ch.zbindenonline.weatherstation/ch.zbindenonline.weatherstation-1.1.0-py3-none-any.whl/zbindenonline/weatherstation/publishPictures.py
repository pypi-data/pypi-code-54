import argparse
import datetime
import logging
import os
import shutil
from pathlib import Path

from zbindenonline.weatherstation.restService import RestServicePictures
from .config import *


def read_configuration():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--wait", help="wait in seconds between publish", type=int, default=300)
    parser.add_argument("-c", "--config", help="config file", type=str, default='weatherstation.cfg')
    parser.add_argument("-l", "--log", help="level to log", type=str, default="INFO")
    args = parser.parse_args()
    return createConfig(args)


def get_pictures(picture_dir):
    logging.info('Parsing ' + picture_dir)
    files = list()
    for file in os.listdir(picture_dir):
        if file.endswith('.jpg'):
            files.append(os.path.join(picture_dir, file))
    return files


def getExistingPictureDir(picture_dir):
    picturesPath = Path(picture_dir)
    return Path(picturesPath, 'existing')


def configure_logging(loglevel):
    numeric_level = getattr(logging, loglevel, "INFO")
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=numeric_level)


class Main:
    def __init__(self, service, pictures, delete_after_publish=False):
        self.service = service
        self.pictures = pictures
        self.delete_after_publish = delete_after_publish

    def run(self, existingPictureDir=None):
        start = datetime.datetime.now()
        try:
            if len(self.pictures) == 0:
                logging.info('Nothing to publish')
            else:
                self.service.login()
                postedPictures = 0
                for picture in self.pictures:
                    logging.debug('Try to publish ' + picture)
                    try:
                        post_result = self.service.post_picture(picture)
                        if post_result == 0:
                            postedPictures += 1
                            if self.delete_after_publish:
                                logging.debug('Delete ' + picture)
                                os.remove(picture)
                        elif post_result == 2:
                            logging.debug('Picture exists already')
                            if existingPictureDir is not None:
                                shutil.move(picture, existingPictureDir, copy_function=shutil.copytree)
                    except Exception as e:
                        logging.warning('There was an Exception in posting picture ' + picture + ': ' + str(e))
                self.service.logout()

                elapsed_time = datetime.datetime.now() - start
                logging.info('Posted ' + str(postedPictures) + ' in ' + str(elapsed_time))
        except Exception as e:
            logging.error("Error occurred: " + str(e))


def main():
    config = read_configuration()
    configure_logging(config.loglevel)
    picture_config = config.pictures
    service = RestServicePictures(picture_config.picture_url, picture_config.camera_id,
                                  picture_config.client_id, picture_config.client_secret,
                                  picture_config.username, picture_config.password)
    pictures = get_pictures(picture_config.picture_dir)
    existingPictureDir = getExistingPictureDir(picture_config.picture_dir)

    Main(service, pictures, picture_config.delete_after_publish).run(existingPictureDir)


if __name__ == '__main__':
    main()
