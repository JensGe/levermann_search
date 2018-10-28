from utils import scrap_op as scrap
from utils import db_op as db


def scrap_index_content_sites():
    scrap_list = db.create_index_content_url_list()
    driver = scrap.init_driver()
    for url in scrap_list:
        file_name = 'data/indizes/' + url.split('/')[-1].replace('?p=','_') + '.html'
        soup = scrap.get_soup_code_of_url(driver, url)
        scrap.save_soup_to_file(soup, file_name)
    scrap.close_driver(driver)
