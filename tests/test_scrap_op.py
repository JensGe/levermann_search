import unittest
from utils import scrap_op as scrap


class TestScrapping(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_data_available_info(self):
        soup = scrap.get_soup_code_from_file('data/no_history_data.html')
        self.assertEqual(False, scrap.is_data_available(soup))

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
