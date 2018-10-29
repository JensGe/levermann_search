from utils import scrap_op as scrap
from utils import db_op as db
from utils import constants as CST


def scrap_index_content_sites():
    scrap_list = db.create_index_content_url_list(CST.URL_INDEX_CONTENT)
    driver = scrap.init_driver()
    for url in scrap_list:
        file_name = CST.INDEX_CONTENT_PATH + url.split('/')[-1] + CST.EXT_HTML
        soup = scrap.get_soup_code_of_url(driver, url)
        scrap.save_soup_to_file(soup, file_name)
    scrap.close_driver(driver)


def scrap_index_content_histories():
    scrap_list = db.create_index_content_url_list(CST.URL_INDEX_HISTORY)
    driver = scrap.init_driver()
    for url in scrap_list:
        file_name = CST.INDEX_HISTORY_PATH + url.split('/')[-1] + CST.EXT_HTML
        soup = scrap.get_soup_code_of_url(driver, url)
        scrap.save_soup_to_file(soup, file_name)
    scrap.close_driver(driver)