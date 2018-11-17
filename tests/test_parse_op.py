import unittest
from utils import scrap_op as scrap
from utils import parse_op as parse
from utils import date_op as date
import re


class TestScrapping(unittest.TestCase):

    def setUp(self):
        pass

    def test_index_history_list_extract(self):
        soup = scrap.get_soup_code_from_file('data/bo_index_history.html')
        history_table = soup.find_all('div', {'id': 'historic-price-list'})
        table_list = parse.extract_history_table_to_list(history_table)
        asserted_list = [['06.09.2018', '11.955,25', '11.995,81', '12.091,98', '11.944,50'],
                         ['07.09.2018', '11.959,63', '11.960,10', '11.990,81', '11.888,57'],
                         ['10.09.2018', '11.986,34', '11.950,55', '12.039,22', '11.930,30'],
                         ['11.09.2018', '11.970,27', '12.013,01', '12.017,73', '11.865,47'],
                         ['12.09.2018', '12.032,30', '11.989,27', '12.046,66', '11.952,49']]
        self.assertEqual(asserted_list, table_list[:5])

    # def test_index_stocks_list_extract(self):
    #     soup = scrap.get_soup_code_of_file('data/bo_index_stocks.html')
    #     stocks_table = soup.find_all('div', {'id': 'index-list-container'})
    #     table_list = parse.extract_index_stocks_to_list(stocks_table)
    #     asserted_list = [['adidas', 'DE000A1EWWW0', 'adidas-Aktie'],
    #                      ['Allianz', 'DE0008404005', 'allianz-Aktie'],
    #                      ['BASF', 'DE000BASF111', 'basf-Aktie'],
    #                      ['Bayer', 'DE000BAY0017', 'bayer-Aktie'],
    #                      ['Beiersdorf', 'DE0005200000', 'beiersdorf-Aktie']]
    #     self.assertEqual(table_list[:5], asserted_list)

    def test_pagination_getting(self):
        soup = scrap.get_soup_code_from_file('data/bo_index_stocks_pagination.html')
        highest_pagination = scrap.get_max_page(soup)
        self.assertEqual(3, highest_pagination)

    def test_get_market_cap(self):
        soup = scrap.get_soup_code_from_file('data/bo_tesla-aktie.html')
        market_cap_value = parse.get_market_cap(soup)
        asserted_market_cap = '37,53 Mrd'
        self.assertEqual(asserted_market_cap, market_cap_value)

    def test_convert_market_cap(self):
        market_cap_string = '37,53 Mrd'
        asserted_marked_cap = 37530
        calc_marked_cap = parse.convert_market_cap(market_cap_string)
        self.assertEqual(asserted_marked_cap, calc_marked_cap)

        market_cap_string_2 = '727,68 Mio'
        asserted_marked_cap_2 = 727.68
        calc_marked_cap_2 = parse.convert_market_cap(market_cap_string_2)
        self.assertEqual(asserted_marked_cap_2, calc_marked_cap_2)

        market_cap_string_2 = '981 Tsd'
        asserted_marked_cap_2 = 0.981
        calc_marked_cap_2 = parse.convert_market_cap(market_cap_string_2)
        self.assertEqual(asserted_marked_cap_2, calc_marked_cap_2)

    def test_stock_in_which_index_multiple(self):
        soup = scrap.get_soup_code_from_file('data/bo_sap-aktie.html')
        link_items = parse.get_listed_indizes(soup)
        asserted_indizes_values = ['TecDAX', 'DAX', 'STOXX 50', 'EURO STOXX 50', 'S&P 400 MidCap',
                                   'EURO STOXX Technology', 'Prime All Share', 'LDAX', 'LTecDAX',
                                   'HDAX', 'DivDAX','NYSE International 100','CDAX','EURO STOXX',
                                   'TecDAX Kursindex', 'DAX Kursindex', 'BX Swiss -  EMEA', 'XDAX',
                                   'DAXglobal Sarasin Sustainability Germany Index EUR', 'L&S DAX Indikation',
                                   'QIX Deutschland', 'DAXglobal Sarasin Sustainability Germany',
                                   'Schatten-Index-TecDAX']

        self.assertEqual(asserted_indizes_values, link_items)

    def test_stock_sectors(self):
        soup = scrap.get_soup_code_from_file('data/bo_sap-aktie.html')
        link_items = parse.get_sectors(soup)
        asserted_indizes_values = ['Informationstechnologie', 'IT-Dienstleister',
                                   'Server-/ Großrechner (Software)', 'Software']
        self.assertEqual(asserted_indizes_values, link_items)

        soup_2 = scrap.get_soup_code_from_file('data/bo_ab_inbev-aktie.html')
        link_items_2 = parse.get_sectors(soup_2)
        asserted_indizes_values_2 = ['Getränke / Tabak']
        self.assertEqual(asserted_indizes_values_2, link_items_2)


    def test_get_result_after_tax(self):
        soup = scrap.get_soup_code_from_file('data/bo_bilanz_guv.html')
        result = parse.get_result_after_tax(soup)
        asserted_result = '1353'
        self.assertEqual(asserted_result, result)

    def test_get_operative_result(self):
        soup = scrap.get_soup_code_from_file('data/bo_bilanz_guv.html')
        result = parse.get_operative_result(soup)
        asserted_result = '1907,4'
        self.assertEqual(asserted_result, result)

    def test_get_sales_revenue(self):
        soup = scrap.get_soup_code_from_file('data/bo_bilanz_guv.html')
        result = parse.get_sales_revenue(soup)
        asserted_result = '21218'
        self.assertEqual(asserted_result, result)

    def test_get_total_assets(self):
        soup = scrap.get_soup_code_from_file('data/bo_bilanz_guv.html')
        result = parse.get_total_assets(soup)
        asserted_result = '14522'
        self.assertEqual(asserted_result, result)

    # ToDo Eigenkapital aus Bilanzseite ziehen
    def test_get_equity_capital(self):
        soup = scrap.get_soup_code_from_file('data/bo_unternehmensprofil.html')
        result = parse.get_current_value_of_attribute(soup, 'Eigenkapital')
        asserted_result = '6.435'
        self.assertEqual(asserted_result, result)

    def test_get_last_quarterly_figures_date(self):
        soup = scrap.get_soup_code_from_file('data/bo_termine.html')
        result = parse.get_last_quarterly_figures_date(soup)
        asserted_result = date.string_to_date('09.08.18')
        self.assertEqual(asserted_result, result)

    def test_get_result_per_share_last_three_years(self):
        soup = scrap.get_soup_code_from_file('data/bo_bilanz_guv.html')
        result_2015, result_2016, result_2017 = parse.get_result_per_share_last_three_years(soup)
        asserted_result_2015 = '3,3'
        asserted_result_2016 = '5,08'
        asserted_result_2017 = '6,69'
        self.assertEqual(asserted_result_2015, result_2015)
        self.assertEqual(asserted_result_2016, result_2016)
        self.assertEqual(asserted_result_2017, result_2017)

    def test_get_result_per_share_current_and_next_year(self):
        soup = scrap.get_soup_code_from_file('data/bo_schaetzungen.html')
        result_2018, result_2019 = parse.get_result_per_share_current_and_next_year(soup)
        asserted_result_2018 = '8,22'
        asserted_result_2019 = '9,54'
        self.assertEqual(asserted_result_2018, result_2018)
        self.assertEqual(asserted_result_2019, result_2019)

    # ToDo Analystenmeinungen aus Overview ziehen
    def test_get_analyst_ratings(self):
        soup = scrap.get_soup_code_from_file('data/bo_kursziele.html')
        no_buy, no_hold, no_sell = parse.get_analyst_ratings(soup)
        asserted_no_buy = '15'
        asserted_no_hold = '8'
        asserted_no_sell = '0'
        self.assertEqual(asserted_no_buy, no_buy)
        self.assertEqual(asserted_no_hold, no_hold)
        self.assertEqual(asserted_no_sell, no_sell)

    def test_get_closing_price_from_date(self):
        soup = scrap.get_soup_code_from_file('data/bo_kurse.html')
        closing_price = parse.get_closing_price_from_date(soup, '09.08.2018')
        asserted_price = '208,50'
        self.assertEqual(asserted_price, closing_price)

    def test_get_closing_price_from_date_before(self):
        soup = scrap.get_soup_code_from_file('data/bo_kurse.html')
        closing_price = parse.get_closing_price_from_date_before(soup, '09.08.2018')
        asserted_price = '190,55'
        self.assertEqual(asserted_price, closing_price)

    def test_get_stock_table_of_index(self):
        soup = scrap.get_soup_code_from_file('data/bo_FTSE_100.html')
        asserted_stock_list_first = [['3i', 'GB00B1YW4409', '3i-Aktie'],
                                     ['Admiral Group', 'GB00B02J6398', 'admiral_group-Aktie'],
                                     ['Anglo American', 'GB00B1XZS820', 'anglo_american-Aktie']]
        asserted_stock_list_last = [['WPP 2012', 'JE00B8KF9B49', 'wpp_2012-Aktie'],
                                    ['WPP 2012', 'JE00B8KF9B49', 'wpp_2012-Aktie']]

        stock_list = parse.get_stock_list_of_single_index(soup)
        self.assertEqual(asserted_stock_list_first, stock_list[:3])
        self.assertEqual(asserted_stock_list_last, stock_list[-2:])

    def test_get_historic_prices(self):
        soup = scrap.get_soup_code_from_file('data/bo_index_history_big.html')
        table_list = parse.get_historic_prices(soup)
        asserted_list = [['01.10.2018', '9.127,05', '9.094,28', '9.155,65', '9.084,22'],
                         ['02.10.2018', '9.087,32', '9.076,57', '9.090,46', '9.050,50'],
                         ['03.10.2018', '9.175,21', '9.126,31', '9.194,99', '9.123,48']]
        self.assertEqual(asserted_list, table_list[:3])

    def test_convert_index_history_list(self):
        insert_list = [['01.10.2018', '9.127,05', '9.094,28', '9.155,65', '9.084,22'],
                       ['02.10.2018', '9.087,32', '9.076,57', '9.090,46', '9.050,50'],
                       ['03.10.2018', '9.175,21', '9.126,31', '9.194,99', '9.123,48']]
        asserted_list = [['01.10.2018', 9127.05, 9094.28],
                         ['02.10.2018', 9087.32, 9076.57],
                         ['03.10.2018', 9175.21, 9126.31]]
        self.assertEqual(asserted_list, parse.convert_index_history_list(insert_list))

    # def test_get_historic_prices_big_html(self):
    #     soup = scrap.get_soup_code_of_file('data/bo_index_history_big.html')
    #     table_list = parse.get_historic_prices(soup)
    #     asserted_list = [['01.10.2018', '9.127,05', '9.094,28', '9.155,65', '9.084,22'],
    #                      ['02.10.2018', '9.087,32', '9.076,57', '9.090,46', '9.050,50'],
    #                      ['03.10.2018', '9.175,21', '9.126,31', '9.194,99', '9.123,48']]
    #     self.assertEqual(table_list[:3], asserted_list)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
