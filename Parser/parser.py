from utils import parse_op as parse
from utils import db_op as db
from utils import scrap_op as scrap


def write_index_contents_from_html_to_db():
    index_list = db.get_index_names()
    file_list = ['data/indizes/' + index for index in index_list]

    for file in file_list:
        index_content_soup = scrap.get_soup_code_of_file(file)
        stock_list = parse.get_stock_list_of_single_index(index_content_soup)
        index_name = file.split('/')[-1]
        db.write_stock_list_to_db(stock_list, index_name)

    return True