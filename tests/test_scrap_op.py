import unittest
from utils import scrap_op as scrap
from utils import date_op as date


class TestScrapping(unittest.TestCase):

    def setUp(self):
        pass

    def test_create_download_list(self):
        stock_short_link = 'allianz-Aktie'
        date_today = date.get_todays_date()
        date_before_one_year = date.subtract_one_year(date_today)
        date_today_str = date.date_to_string(date_today)
        date_before_one_year_str = date.date_to_string(date_before_one_year)
        download_list = scrap.create_download_list(stock_short_link)
        asserted_list = ['https://www.boerse-online.de/aktie/allianz-Aktie',
                         'https://www.boerse-online.de/kurse/historisch/allianz/xetra/' + date_before_one_year_str + '_' + date_today_str,
                         'https://www.boerse-online.de/bilanz_guv/allianz',
                         'https://www.boerse-online.de/schaetzungen/allianz',
                         'https://www.boerse-online.de/unternehmensprofil/allianz',
                         'https://www.boerse-online.de/termine/uebersicht/allianz']
        self.assertEqual(download_list, asserted_list)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
