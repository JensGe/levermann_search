import unittest
from utils import scrap_op as scrap
from utils import parse_op as parse
from utils import date_op as date


class TestScrapping(unittest.TestCase):
    def setUp(self):
        pass

    def test_index_stocks_list_extract(self):
        soup = scrap.get_soup_code_from_file("data/bo_index_stocks.html")
        stocks_table = soup.find_all("div", {"id": "index-list-container"})
        table_list = parse.extract_index_stocks_to_list(stocks_table)
        asserted_list = [
            ["adidas", "adidas-Aktie"],
            ["Allianz", "allianz-Aktie"],
            ["BASF", "basf-Aktie"],
            ["Bayer", "bayer-Aktie"],
            ["Beiersdorf", "beiersdorf-Aktie"],
        ]
        self.assertEqual(table_list[:5], asserted_list)

    def test_pagination_getting(self):
        soup = scrap.get_soup_code_from_file("data/bo_index_stocks_pagination.html")
        highest_pagination = scrap.get_max_page(soup)
        self.assertEqual(3, highest_pagination)

    def test_get_market_cap(self):
        soup = scrap.get_soup_code_from_file("data/bo_tesla-aktie.html")
        market_cap_value = parse.get_market_cap(soup)
        asserted_market_cap = 37530
        self.assertEqual(asserted_market_cap, market_cap_value)

        soup2 = scrap.get_soup_code_from_file("data/bo_3i-Aktie_overview.html")
        market_cap_value2 = parse.get_market_cap(soup2)
        asserted_market_cap2 = 9600
        self.assertEqual(asserted_market_cap2, market_cap_value2)

        soup3 = scrap.get_soup_code_from_file(
            "data/bo_london_stock_exchange-Aktie_overview.html"
        )
        market_cap_value3 = parse.get_market_cap(soup3)
        asserted_market_cap3 = 15890
        self.assertEqual(asserted_market_cap3, market_cap_value3)

    def test_get_market_place(self):
        soup3 = scrap.get_soup_code_from_file("data/bo_aes-Aktie_overview.html")
        market_place3 = parse.get_market_place(soup3)
        asserted_market_place3 = "FSE"
        self.assertEqual(asserted_market_place3, market_place3)

    def test_convert_market_cap(self):
        market_cap_string = "37,53 Mrd"
        asserted_marked_cap = 37530
        calc_marked_cap = parse.convert_market_cap(market_cap_string)
        self.assertEqual(asserted_marked_cap, calc_marked_cap)

        market_cap_string_2 = "727,68 Mio"
        asserted_marked_cap_2 = 727.68
        calc_marked_cap_2 = parse.convert_market_cap(market_cap_string_2)
        self.assertEqual(asserted_marked_cap_2, calc_marked_cap_2)

        market_cap_string_2 = "981 Tsd"
        asserted_marked_cap_2 = 0.981
        calc_marked_cap_2 = parse.convert_market_cap(market_cap_string_2)
        self.assertEqual(asserted_marked_cap_2, calc_marked_cap_2)

    def test_stock_in_which_index_multiple(self):
        soup = scrap.get_soup_code_from_file("data/bo_sap-aktie.html")
        link_items = parse.get_listed_indizes(soup)
        asserted_idx_values = [
            "TecDAX",
            "DAX",
            "STOXX 50",
            "EURO STOXX 50",
            "S&P 400 MidCap",
            "EURO STOXX Technology",
            "Prime All Share",
            "LDAX",
            "LTecDAX",
            "HDAX",
            "DivDAX",
            "NYSE International 100",
            "CDAX",
            "EURO STOXX",
            "TecDAX Kursindex",
            "DAX Kursindex",
            "BX Swiss -  EMEA",
            "XDAX",
            "DAXglobal Sarasin Sustainability Germany Index EUR",
            "L&S DAX Indikation",
            "QIX Deutschland",
            "DAXglobal Sarasin Sustainability Germany",
            "Schatten-Index-TecDAX",
        ]

        self.assertEqual(asserted_idx_values, link_items)

        soup2 = scrap.get_soup_code_from_file("data/bo_3i-Aktie_overview.html")
        link_items2 = parse.get_listed_indizes(soup2)
        asserted_indizes_values2 = ["FTSE 100", "FTSE Allshare"]
        self.assertEqual(asserted_indizes_values2, link_items2)

    def test_stock_sectors(self):
        soup = scrap.get_soup_code_from_file("data/bo_sap-aktie.html")
        link_items = parse.get_sectors(soup)
        asserted_indizes_values = [
            "Informationstechnologie",
            "IT-Dienstleister",
            "Server-/ Großrechner (Software)",
            "Software",
        ]
        self.assertEqual(asserted_indizes_values, link_items)

        soup_2 = scrap.get_soup_code_from_file("data/bo_ab_inbev-aktie.html")
        link_items_2 = parse.get_sectors(soup_2)
        asserted_indizes_values_2 = ["Getränke / Tabak"]
        self.assertEqual(asserted_indizes_values_2, link_items_2)

        soup3 = scrap.get_soup_code_from_file("data/bo_3i-Aktie_overview.html")
        link_items3 = parse.get_sectors(soup3)
        asserted_indizes_values3 = ["Finanzdienstleister"]
        self.assertEqual(asserted_indizes_values3, link_items3)

    def test_if_is_data_available(self):
        soup = scrap.get_soup_code_from_file("data/bo_bhp_billiton_balance.html")
        self.assertFalse(parse.is_data_available(soup))

    def test_get_latest_date_of_list(self):
        date_list = [
            date.string_to_date("09.08.2018"),
            date.string_to_date("09.05.2018"),
            date.string_to_date("09.11.2017"),
        ]
        current_date = date.string_to_date("11.10.2018")
        latest_date = parse.get_latest_date_of_list(date_list, current_date)
        self.assertEqual(date.string_to_date("09.08.2018"), latest_date)

    def test_get_result_after_tax(self):
        soup = scrap.get_soup_code_from_file("data/bo_bilanz_guv.html")
        result = parse.get_current_value_of_attribute(soup, "Ergebnis nach Steuer")
        asserted_result = 1353
        self.assertEqual(asserted_result, result)

    def test_get_operative_result(self):
        soup = scrap.get_soup_code_from_file("data/bo_bilanz_guv.html")
        result = parse.get_current_value_of_attribute(soup, "Operatives Ergebnis")
        asserted_result = 1907.4
        self.assertEqual(asserted_result, result)

    def test_get_sales_revenue(self):
        soup = scrap.get_soup_code_from_file("data/bo_bilanz_guv.html")
        result = parse.get_current_value_of_attribute(soup, "Umsatzerlöse")
        asserted_result = 21218
        self.assertEqual(asserted_result, result)

    def test_get_total_assets(self):
        soup = scrap.get_soup_code_from_file("data/bo_bilanz_guv.html")
        result = parse.get_current_value_of_attribute(soup, "Bilanzsumme")
        asserted_result = 14522
        self.assertEqual(asserted_result, result)

    def test_get_equity_capital_new(self):
        soup = scrap.get_soup_code_from_file("data/bo_bilanz_guv.html")
        result = parse.get_current_value_of_attribute(soup, "Eigenkapital")
        asserted_result = 6435
        self.assertEqual(asserted_result, result)

    def test_get_last_quarterly_figures_date(self):
        soup = scrap.get_soup_code_from_file("data/bo_termine.html")
        result = parse.get_last_quarterly_figures_date(
            soup=soup, current_date=date.string_to_date("10.10.2018")
        )
        asserted_result = date.string_to_date("09.08.18")
        self.assertEqual(asserted_result, result)

    def test_get_future_dates(self):
        soup = scrap.get_soup_code_from_file("data/bo_termine.html")
        result = parse.get_future_dates(soup)
        asserted_result = [
            ["adidas AG", "2018-11-07", "Quartalszahlen", "Future"],
            ["adidas AG", "2019-03-07", "Quartalszahlen", "Future"],
            ["adidas AG", "2019-05-02", "Quartalszahlen", "Future"],
            ["adidas AG", "2019-05-09", "Hauptversammlung", "Future"],
            ["adidas AG", "2019-08-08", "Quartalszahlen", "Future"],
            ["adidas AG", "2019-11-07", "Quartalszahlen", "Future"],
        ]
        self.assertEqual(asserted_result, result)

    def test_get_bygone_dates(self):
        soup = scrap.get_soup_code_from_file("data/bo_termine.html")
        result = parse.get_bygone_dates(soup)
        asserted_result = [
            ["adidas AG", "2018-08-09", "Q2 2018 Earnings Release", "Past"],
            ["adidas AG", "2018-05-09", "Hauptversammlung", "Past"],
            ["adidas AG", "2017-11-09", "Q3 2017", "Past"],
        ]
        self.assertEqual(asserted_result, result)

    def test_get_result_per_share_last_three_years(self):
        soup = scrap.get_soup_code_from_file("data/bo_bilanz_guv.html")
        result_15, result_16, result_17 = parse.get_result_per_share_last_three_years(
            soup
        )
        asserted_result_2015 = 3.3
        asserted_result_2016 = 5.08
        asserted_result_2017 = 6.69
        self.assertEqual(asserted_result_2015, result_15)
        self.assertEqual(asserted_result_2016, result_16)
        self.assertEqual(asserted_result_2017, result_17)

    def test_get_result_per_share_current_and_next_year(self):
        soup = scrap.get_soup_code_from_file("data/bo_schaetzungen.html")
        result_2018, result_2019 = parse.get_result_per_share_current_and_next_year(
            soup
        )
        asserted_result_2018 = 8.22
        asserted_result_2019 = 9.54
        self.assertEqual(asserted_result_2018, result_2018)
        self.assertEqual(asserted_result_2019, result_2019)

    def test_get_analyst_ratings(self):
        soup = scrap.get_soup_code_from_file("data/bo_kursziele.html")
        no_buy, no_hold, no_sell = parse.get_analyst_ratings(soup)
        asserted_no_buy = 15
        asserted_no_hold = 8
        asserted_no_sell = 0
        self.assertEqual(asserted_no_buy, no_buy)
        self.assertEqual(asserted_no_hold, no_hold)
        self.assertEqual(asserted_no_sell, no_sell)

    def test_get_closing_price_from_date(self):
        soup = scrap.get_soup_code_from_file("data/bo_kurse.html")
        closing_price = parse.get_closing_price_from_date(soup, "09.08.2018")
        asserted_price = 208.50
        self.assertEqual(asserted_price, closing_price)

    def test_get_closing_price_from_date_before(self):
        soup = scrap.get_soup_code_from_file("data/bo_kurse.html")
        closing_price = parse.get_closing_price_from_date_before(soup, "09.08.2018")
        asserted_price = 190.55
        self.assertEqual(asserted_price, closing_price)

    def test_get_stock_table_of_index(self):
        soup = scrap.get_soup_code_from_file("data/bo_FTSE_100.html")
        asserted_stock_list_first = [
            ["3i", "3i-Aktie"],
            ["Admiral Group", "admiral_group-Aktie"],
            ["Anglo American", "anglo_american-Aktie"],
        ]
        asserted_stock_list_last = [
            ["WPP 2012", "wpp_2012-Aktie"],
            ["WPP 2012", "wpp_2012-Aktie"],
        ]

        stock_list = parse.get_stock_list_of_single_index(soup)
        self.assertEqual(asserted_stock_list_first, stock_list[:3])
        self.assertEqual(asserted_stock_list_last, stock_list[-2:])

    def test_get_historic_prices(self):
        soup = scrap.get_soup_code_from_file("data/bo_index_history_big.html")
        table_list = parse.get_historic_prices_from_history(soup)
        asserted_list = [
            ["01.10.2018", "9.127,05", "9.094,28", "9.155,65", "9.084,22"],
            ["02.10.2018", "9.087,32", "9.076,57", "9.090,46", "9.050,50"],
            ["03.10.2018", "9.175,21", "9.126,31", "9.194,99", "9.123,48"],
        ]
        self.assertEqual(asserted_list, table_list[:3])

    def test_get_historic_prices_from_overview(self):
        soup = scrap.get_soup_code_from_file("data/bo_3i-Aktie_overview.html")
        table_list = parse.get_historic_stock_prices_from_overview(soup)
        asserted_list = [
            ["29.11.2018", "9,87"],
            ["28.11.2018", "9,69"],
            ["27.11.2018", "9,75"],
            ["26.11.2018", "9,62"],
            ["23.11.2018", "9,44"],
        ]
        self.assertEqual(asserted_list, table_list)

    def test_convert_index_history_list(self):
        insert_list = [
            ["01.10.2018", "9.127,05", "9.094,28", "9.155,65", "9.084,22"],
            ["02.10.2018", "9.087,32", "9.076,57", "9.090,46", "9.050,50"],
            ["03.10.2018", "9.175,21", "9.126,31", "9.194,99", "9.123,48"],
        ]
        asserted_list = [
            ["01.10.2018", 9127.05, 9094.28],
            ["02.10.2018", 9087.32, 9076.57],
            ["03.10.2018", 9175.21, 9126.31],
        ]
        self.assertEqual(asserted_list, parse.convert_index_history_list(insert_list))

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
