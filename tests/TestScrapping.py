import unittest
from utils import file_op as file
from utils import local_scrap_op as scrap
from Scrapper import index_history_scrapper as ihs
from bs4 import BeautifulSoup


class TestScrapping(unittest.TestCase):

    def setUp(self):
        pass

    def test_index_history_list_extract(self):
        content = scrap.get_content_from_file("data/bo_index_history.html")
        soup = scrap.create_soup_from_content(content)
        history_table = soup.find_all("div", {"id": "historic-price-list"})
        table_list = ihs.extract_history_table_to_list(history_table)
        asserted_list = [['06.09.2018', '11.955,25', '11.995,81', '12.091,98', '11.944,50'],
                         ['07.09.2018', '11.959,63', '11.960,10', '11.990,81', '11.888,57'],
                         ['10.09.2018', '11.986,34', '11.950,55', '12.039,22', '11.930,30'],
                         ['11.09.2018', '11.970,27', '12.013,01', '12.017,73', '11.865,47'],
                         ['12.09.2018', '12.032,30', '11.989,27', '12.046,66', '11.952,49']]
        self.assertEqual(table_list[:5], asserted_list)

    def test_index_stocks_list_extract(self):
        content = scrap.get_content_from_file("data/bo_index_stocks.html")
        soup = scrap.create_soup_from_content(content)
        stocks_table = soup.find_all("div", {"id": "index-list-container"})
        table_list = ihs.extract_index_stocks_to_list(stocks_table)
        asserted_list = [['adidas', 'DE000A1EWWW0', 'adidas-Aktie'],
                         ['Allianz', 'DE0008404005', 'allianz-Aktie'],
                         ['BASF', 'DE000BASF111', 'basf-Aktie'],
                         ['Bayer', 'DE000BAY0017', 'bayer-Aktie'],
                         ['Beiersdorf', 'DE0005200000', 'beiersdorf-Aktie']]
        self.assertEqual(table_list[:5], asserted_list)

    def test_pagination_getting(self):
        content = scrap.get_content_from_file("data/bo_index_stocks_pagination.html")
        soup = scrap.create_soup_from_content(content)
        highest_pagination = ihs.get_max_page(soup)
        self.assertEqual(highest_pagination, 3)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
