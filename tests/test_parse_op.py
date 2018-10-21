import unittest
from utils import scrap_op as scrap
from utils import parse_op as parse
import re


class TestScrapping(unittest.TestCase):

    def setUp(self):
        pass

    def test_index_history_list_extract(self):
        soup = scrap.get_soup_code_of_file('data/bo_index_history.html')
        history_table = soup.find_all('div', {'id': 'historic-price-list'})
        table_list = parse.extract_history_table_to_list(history_table)
        asserted_list = [['06.09.2018', '11.955,25', '11.995,81', '12.091,98', '11.944,50'],
                         ['07.09.2018', '11.959,63', '11.960,10', '11.990,81', '11.888,57'],
                         ['10.09.2018', '11.986,34', '11.950,55', '12.039,22', '11.930,30'],
                         ['11.09.2018', '11.970,27', '12.013,01', '12.017,73', '11.865,47'],
                         ['12.09.2018', '12.032,30', '11.989,27', '12.046,66', '11.952,49']]
        self.assertEqual(table_list[:5], asserted_list)

    def test_index_stocks_list_extract(self):
        soup = scrap.get_soup_code_of_file('data/bo_index_stocks.html')
        stocks_table = soup.find_all('div', {'id': 'index-list-container'})
        table_list = parse.extract_index_stocks_to_list(stocks_table)
        asserted_list = [['adidas', 'DE000A1EWWW0', 'adidas-Aktie'],
                         ['Allianz', 'DE0008404005', 'allianz-Aktie'],
                         ['BASF', 'DE000BASF111', 'basf-Aktie'],
                         ['Bayer', 'DE000BAY0017', 'bayer-Aktie'],
                         ['Beiersdorf', 'DE0005200000', 'beiersdorf-Aktie']]
        self.assertEqual(table_list[:5], asserted_list)

    def test_pagination_getting(self):
        soup = scrap.get_soup_code_of_file('data/bo_index_stocks_pagination.html')
        highest_pagination = parse.get_max_page(soup)
        self.assertEqual(highest_pagination, 3)

    def test_get_market_cap(self):
        soup = scrap.get_soup_code_of_file('data/bo_tesla-aktie.html')
        market_cap_title = soup.find(text=re.compile('Marktkapitalisierung'))
        market_cap_value = market_cap_title.find_next('td').contents[0].strip()
        asserted_market_cap = '37,53 Mrd'
        self.assertEqual(asserted_market_cap, market_cap_value)

    def test_stock_in_which_index_multiple(self):
        soup = scrap.get_soup_code_of_file('data/bo_sap-aktie.html')
        indizes = soup.find_all('h2', text=re.compile('Zur Aktie'))
        parent = []
        for par in indizes:
            parent.append(par.parent)
        link_items = []
        for items in parent:
            links = items.find_all('a')
            for link in links:
                link_items.append(link.text)

        asserted_indizes_values = ['TecDAX', 'DAX', 'STOXX 50', 'EURO STOXX 50', 'S&P 400 MidCap',
                                   'EURO STOXX Technology', 'Prime All Share', 'LDAX', 'LTecDAX',
                                   'HDAX', 'DivDAX','NYSE International 100','CDAX','EURO STOXX',
                                   'TecDAX Kursindex', 'DAX Kursindex', 'BX Swiss -  EMEA', 'XDAX',
                                   'DAXglobal Sarasin Sustainability Germany Index EUR', 'L&S DAX Indikation',
                                   'QIX Deutschland', 'DAXglobal Sarasin Sustainability Germany',
                                   'Schatten-Index-TecDAX']

        self.assertEqual(asserted_indizes_values, link_items)

    def test_stock_sectors(self):
        soup = scrap.get_soup_code_of_file('data/bo_sap-aktie.html')
        indizes = soup.find_all('h2', text=re.compile('Zum Unternehmen'))
        parent = []
        for par in indizes:
            parent.append(par.parent)
        link_items = []
        for items in parent:
            links = items.find_all('a')
            for link in links:
                link_items.append(link.text)

        asserted_indizes_values = ['Informationstechnologie', 'IT-Dienstleister',
                                   'Server-/ Großrechner (Software)', 'Software']
        self.assertEqual(asserted_indizes_values, link_items)

    def test_get_historic_prices(self):
        soup = scrap.get_soup_code_of_file('data/bo_index_history.html')
        table_list = parse.get_historic_prices(soup)
        asserted_list = [['06.09.2018', '11.955,25', '11.995,81', '12.091,98', '11.944,50'],
                         ['07.09.2018', '11.959,63', '11.960,10', '11.990,81', '11.888,57'],
                         ['10.09.2018', '11.986,34', '11.950,55', '12.039,22', '11.930,30'],
                         ['11.09.2018', '11.970,27', '12.013,01', '12.017,73', '11.865,47'],
                         ['12.09.2018', '12.032,30', '11.989,27', '12.046,66', '11.952,49']]
        self.assertEqual(table_list[:5], asserted_list)

    def test_get_result_after_tax(self):
        soup = scrap.get_soup_code_of_file('data/bo_bilanz_guv.html')
        result = parse.get_result_after_tax(soup)
        asserted_result = '1353'
        self.assertEqual(result, asserted_result)

    def test_get_operative_result(self):
        soup = scrap.get_soup_code_of_file('data/bo_bilanz_guv.html')
        result = parse.get_operative_result(soup)
        asserted_result = '1907,4'
        self.assertEqual(result, asserted_result)

    def test_get_sales_revenue(self):
        soup = scrap.get_soup_code_of_file('data/bo_bilanz_guv.html')
        result = parse.get_sales_revenue(soup)
        asserted_result = '21218'
        self.assertEqual(result, asserted_result)

    def test_get_total_assets(self):
        soup = scrap.get_soup_code_of_file('data/bo_bilanz_guv.html')
        result = parse.get_total_assets(soup)
        asserted_result = '14522'
        self.assertEqual(result, asserted_result)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
