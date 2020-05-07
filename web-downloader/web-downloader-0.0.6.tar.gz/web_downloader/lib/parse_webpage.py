import os
# import db
from . import db
from . import paths_management as paths
from selenium import webdriver

def parse_url(url_id, depth_level):
    app_paths = paths.App_Paths()
    curr_db = db.Database()
    url_obj = curr_db.get_url(url_id)
    local_url = url_obj['file_path']

    assert app_paths.firefox_driver_path is not None

    with webdriver.Firefox(executable_path=app_paths.firefox_driver_path) as driver:
        driver.get(f'file://{local_url}')
        # elems = driver.find_elements_by_xpath("//a[@href]")
        elems = driver.find_elements_by_tag_name('a')

        parsed_url_saved_counter = 0

        for elem in elems:
            href = elem.get_attribute('href')
            if href is not None:
                # print(href)
                curr_db.insert_url_from_parsing(url_id, href, -1, elem.get_attribute('innerText'), depth_level)
                parsed_url_saved_counter += 1


    print(f'Number of parsed urls: {parsed_url_saved_counter}')