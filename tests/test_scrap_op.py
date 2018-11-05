import unittest
from utils import scrap_op as scrap
from utils import date_op as date


class TestScrapping(unittest.TestCase):

    def setUp(self):
        pass

    def test_create_stock_download_list(self):
        stock_short_link = 'allianz-Aktie'
        date_today = date.get_todays_date()
        date_before_one_year = date.subtract_one_year(date_today)
        date_today_str = date.date_to_string(date_today)
        date_before_one_year_str = date.date_to_string(date_before_one_year)
        download_list = scrap.create_stock_download_list(stock_short_link)
        asserted_list = ['https://www.boerse-online.de/aktie/allianz-Aktie',
                         'https://www.boerse-online.de/kurse/historisch/allianz/xetra/' + date_before_one_year_str + '_' + date_today_str,
                         'https://www.boerse-online.de/bilanz_guv/allianz',
                         'https://www.boerse-online.de/schaetzungen/allianz',
                         'https://www.boerse-online.de/unternehmensprofil/allianz',
                         'https://www.boerse-online.de/termine/uebersicht/allianz',
                         'https://www.boerse-online.de/kursziele/allianz']
        self.assertEqual(asserted_list, download_list)

    def test_get_data_available_info(self):
        soup = scrap.get_soup_code_from_file('data/no_history_data.html')
        self.assertEqual(False, scrap.get_data_available_info(soup))


    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
