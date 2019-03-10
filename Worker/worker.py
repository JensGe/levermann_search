from utils import scrap_op as scrap
from utils import db_op as db




def start_complete_workflow():
    stock_list = db.get_working_stock_list()


