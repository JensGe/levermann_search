from Scraper import scraper
from Parser import parser
from Calculator import calculator
from Displayer import displayer
from utils import constants as CST
from loguru import logger


logger.configure(handlers=[dict(sink="logs/levermann_{time:YYYY-DDDD}.log",
                                format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
                                rotation="weekly", level="INFO")],
                 activation=[("Displayer.displayer", True), ("Parser.parser", True), ("Calculator.calculator", True),
                             ("utils.date_op", True), ("utils.db_op", True), ("utils.file_op", True),
                             ("utils.parse_op", True), ("utils.scrap_op", True)])


@logger.catch()
def main():

    root_menu = True

    while root_menu:
        print('Main Menu')
        print('(1) Index Processing')
        print('(2) Stocks Processing')
        print('(3) Calculate')
        print('---------------')
        print('(4) Show Results')
        print('---------------')
        print('(x) Exit')

        menu_selection = str(input('> '))

        if menu_selection == '1':
            menu_1 = True
            while menu_1:
                print('Sub Menu 1: Index Processing')
                print('(1) Scrap Index Contents')
                print('(2) Write Index Contents to DB')
                print('------------------------')
                print('(3) Scrap Index Histories')
                print('(4) Write Index Histories to DB')
                print('------------------------')
                print('(a) Run All')
                print('(u) Up')
                print('(x) Exit')
                menu_1_selection = str(input('> '))
                if menu_1_selection == '1':
                    scraper.scrap_index_content_sites()
                elif menu_1_selection == '2':
                    parser.write_index_contents_from_html_to_db()
                elif menu_1_selection == '3':
                    scraper.scrap_index_histories()
                elif menu_1_selection == '4':
                    parser.write_index_histories_from_html_to_db()
                elif menu_1_selection == 'a':
                    scraper.scrap_index_content_sites()
                    parser.write_index_contents_from_html_to_db()
                    scraper.scrap_index_histories()
                    parser.write_index_histories_from_html_to_db()
                elif menu_1_selection == 'u':
                    menu_1 = False
                elif menu_1_selection == 'x':
                    menu_1 = False
                    root_menu = False

        elif menu_selection == '2':
            menu_2 = True
            while menu_2:
                print('Sub Menu 2: Stock Processing')
                print('(1) Scrap & Write Stock Overview')
                print('(2) Scrap & Write Stock Histories')
                print('(3) Scrap & Write Stock Balance')
                print('(4) Scrap & Write Stock Estimates')
                print('(5) Scrap & Write Stock Targets')
                print('(6) Scrap & Write Stock Dates')
                print('------------------------------')
                print('(a) Run All')
                print('(s) Scrap All')
                print('(p) Parse All')
                print('(u) Up')
                print('(x) Exit')
                menu_2_selection = str(input('> '))
                if menu_2_selection == '1':
                    scraper.scrap_stock_info(CST.URL_STOCK_OVERVIEW, CST.PATH_STOCK_OVERVIEW)
                    parser.write_stock_overview_data_to_db()
                elif menu_2_selection == '2':
                    scraper.scrap_stock_histories()
                    parser.write_stock_histories_from_html_to_db()
                elif menu_2_selection == '3':
                    scraper.scrap_stock_info(CST.URL_STOCK_BALANCE, CST.PATH_STOCK_BALANCE)
                    parser.write_stock_balance_data_to_db()
                elif menu_2_selection == '4':
                    scraper.scrap_stock_info(CST.URL_STOCK_ESTIMATES, CST.PATH_STOCK_ESTIMATES)
                    parser.write_stock_estimates_data_to_db()
                elif menu_2_selection == '5':
                    scraper.scrap_stock_info(CST.URL_STOCK_TARGETS, CST.PATH_STOCK_TARGETS)
                    parser.write_stock_targets_data_to_db()
                elif menu_2_selection == '6':
                    scraper.scrap_stock_info(CST.URL_STOCK_DATES, CST.PATH_STOCK_DATES)
                    parser.write_stock_last_quarterly_figures_date_to_db()
                elif menu_2_selection == 'a':
                    scraper.scrap_stock_info(CST.URL_STOCK_OVERVIEW, CST.PATH_STOCK_OVERVIEW)
                    parser.write_stock_overview_data_to_db()
                    scraper.scrap_stock_histories()
                    parser.write_stock_histories_from_html_to_db()
                    scraper.scrap_stock_info(CST.URL_STOCK_BALANCE, CST.PATH_STOCK_BALANCE)
                    parser.write_stock_balance_data_to_db()
                    scraper.scrap_stock_info(CST.URL_STOCK_ESTIMATES, CST.PATH_STOCK_ESTIMATES)
                    parser.write_stock_estimates_data_to_db()
                    scraper.scrap_stock_info(CST.URL_STOCK_TARGETS, CST.PATH_STOCK_TARGETS)
                    parser.write_stock_targets_data_to_db()
                    scraper.scrap_stock_info(CST.URL_STOCK_DATES, CST.PATH_STOCK_DATES)
                    parser.write_stock_last_quarterly_figures_date_to_db()
                elif menu_2_selection == 's':
                    scraper.scrap_stock_info(CST.URL_STOCK_OVERVIEW, CST.PATH_STOCK_OVERVIEW)
                    scraper.scrap_stock_histories()
                    scraper.scrap_stock_info(CST.URL_STOCK_BALANCE, CST.PATH_STOCK_BALANCE)
                    scraper.scrap_stock_info(CST.URL_STOCK_ESTIMATES, CST.PATH_STOCK_ESTIMATES)
                    scraper.scrap_stock_info(CST.URL_STOCK_TARGETS, CST.PATH_STOCK_TARGETS)
                    scraper.scrap_stock_info(CST.URL_STOCK_DATES, CST.PATH_STOCK_DATES)
                elif menu_2_selection == 'p':
                    parser.write_stock_overview_data_to_db()
                    parser.write_stock_histories_from_html_to_db()
                    parser.write_stock_balance_data_to_db()
                    parser.write_stock_estimates_data_to_db()
                    parser.write_stock_targets_data_to_db()
                    parser.write_stock_last_quarterly_figures_date_to_db()
                elif menu_2_selection == 'u':
                    menu_2 = False
                elif menu_2_selection == 'x':
                    menu_2 = False
                    root_menu = False

        elif menu_selection == '3':
            menu_3 = True
            while menu_3:
                print('Sub Menu 3: Calculate')
                print('#(1) Return on Equity')
                print('#(2) Earnings before Interest and taxes')
                print('#(3) Equity Ratio')
                print('#(4) KGV 5 + KGV 0')
                print('#(5) -')
                print('#(6) Analyst Ratings')
                print('#(7) Quarterly Reaction')
                print('#(8) EPS Revision')
                print('#(9) Stock Change 6 Month + 12 Month + Momentum')
                print('#(10) -')
                print('#(11) -')
                print('#(12) Three Month Reversal')
                print('#(13) Profit Growth')
                print('------------------------')
                print('(a) Run All')
                print('(u) Up')
                print('(x) Exit')
                menu_3_selection = str(input('> '))
                if menu_3_selection == '1':
                    calculator.levermann_01()
                elif menu_3_selection == '2':
                    calculator.levermann_02()
                elif menu_3_selection == '3':
                    calculator.levermann_03()
                elif menu_3_selection == '4':
                    calculator.levermann_04_05()
                elif menu_3_selection == '6':
                    calculator.levermann_06()
                elif menu_3_selection == '7':
                    calculator.levermann_07()
                elif menu_3_selection == '8':
                    calculator.levermann_08()
                elif menu_3_selection == '9':
                    calculator.levermann_09_10_11()
                elif menu_3_selection == '12':
                    calculator.levermann_12()
                elif menu_3_selection == '13':
                    calculator.levermann_13()
                elif menu_3_selection == 'a':
                    calculator.run_all()
                elif menu_3_selection == 'u':
                    menu_3 = False
                elif menu_3_selection == 'x':
                    menu_3 = False
                    root_menu = False

        elif menu_selection == '4':
            menu_4 = True
            while menu_4:
                print('Sub Menu 4: Show Results')
                print('#(1) Show Levermann Buy Recommendation')
                print('#(2) Show Levermann Hold Recommendation (w/o Buy)')
                print('------------------------')
                print('(u) Up')
                print('(x) Exit')
                menu_4_selection = str(input('> '))
                if menu_4_selection == '1':
                    displayer.display_levermann_buy()
                elif menu_4_selection == '2':
                    displayer.display_levermann_hold()
                elif menu_4_selection == 'u':
                    menu_4 = False
                elif menu_4_selection == 'x':
                    menu_4 = False
                    root_menu = False

        elif menu_selection == 'x':
            root_menu = False


if __name__ == '__main__':
    main()
