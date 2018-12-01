from Scraper import scraper
from Parser import parser
from Calculator import calculator
from Displayer import displayer
from utils import constants as CST


root_menu = True

while root_menu:
    print('Main Menu')
    print('(1) Scraping')
    print('(2) Parsing')
    print('(3) Calculate')
    print('---------------')
    print('(4) Show Best Stocks')
    print('---------------')
    print('(x) Exit')

    menu_selection = str(input('> '))

    if menu_selection == '1':
        menu_1 = True
        while menu_1:
            print('Sub Menu 1: Scraping')
            print('(1) Scrap Index Contents')   # OK
            print('(2) Scrap Index Histories')  # OK
            print('------------------------')
            print('(3) Scrap Stock Histories')  # OK
            print('(4) Scrap Stock Infos')      # OK
            print('------------------------')
            print('(5) Scrap Stock Overview')
            print('(6) Scrap Stock Balance')
            print('(7) Scrap Stock Dates')
            print('(8) Scrap Stock Estimates')
            print('(9) Scrap Stock Targets')
            print('------------------------')
            print('(a) Run All')
            print('(u) Up')
            print('(x) Exit')
            menu_1_selection = str(input('> '))
            if menu_1_selection == '1':
                scraper.scrap_index_content_sites()
            elif menu_1_selection == '2':
                scraper.scrap_index_histories()
            elif menu_1_selection == '3':
                scraper.scrap_stock_histories()
            elif menu_1_selection == '4':
                scraper.scrap_stock_infos()
            elif menu_1_selection == '5':
                scraper.scrap_stock_info(CST.URL_STOCK_OVERVIEW, CST.PATH_STOCK_OVERVIEW)
            elif menu_1_selection == '6':
                scraper.scrap_stock_info(CST.URL_STOCK_BALANCE, CST.PATH_STOCK_BALANCE)
            elif menu_1_selection == '7':
                scraper.scrap_stock_info(CST.URL_STOCK_DATES, CST.PATH_STOCK_DATES)
            elif menu_1_selection == '8':
                scraper.scrap_stock_info(CST.URL_STOCK_ESTIMATES, CST.PATH_STOCK_ESTIMATES)
            elif menu_1_selection == '9':
                scraper.scrap_stock_info(CST.URL_STOCK_TARGETS, CST.PATH_STOCK_TARGETS)

            elif menu_1_selection == 'a':
                scraper.scrap_index_content_sites()
                scraper.scrap_index_histories()
                scraper.scrap_stock_histories()
                scraper.scrap_stock_infos()
            elif menu_1_selection == 'u':
                menu_1 = False
            elif menu_1_selection == 'x':
                menu_1 = False
                root_menu = False

    elif menu_selection == '2':
        menu_2 = True
        while menu_2:
            print('Sub Menu 2: Parsing')
            print('(1) Write Index Contents to DB')     # OK
            print('(2) Write Index Histories to DB')    # OK
            print('------------------------------')
            print('(3) Write Stock Histories to DB')    # OK
            print('(4) Write Stock Overview to DB')     # OK
            print('(5) Write Stock Balance to DB')      # OK
            print('(6) Write Stock Estimates to DB')    # OK
            print('(7) Write Stock Targets to DB')      # OK
            print('(8) Write Stock Dates to DB')        # OK
            print('------------------------------')
            print('(a) Run All')
            print('(u) Up')
            print('(x) Exit')
            menu_2_selection = str(input('> '))
            if menu_2_selection == '1':
                parser.write_index_contents_from_html_to_db()
            elif menu_2_selection == '2':
                parser.write_index_histories_from_html_to_db()
            elif menu_2_selection == '3':
                parser.write_stock_histories_from_html_to_db()
            elif menu_2_selection == '4':
                parser.write_stock_overview_data_to_db()
            elif menu_2_selection == '5':
                parser.write_stock_balance_data_to_db()
            elif menu_2_selection == '6':
                parser.write_stock_estimates_data_to_db()
            elif menu_2_selection == '7':
                parser.write_stock_targets_data_to_db()
            elif menu_2_selection == '8':
                parser.write_stock_last_quarterly_figures_date_to_db()
            elif menu_2_selection == 'a':
                parser.write_index_contents_from_html_to_db()
                parser.write_index_histories_from_html_to_db()
                parser.write_stock_histories_from_html_to_db()
                parser.write_stock_overview_data_to_db()
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
            elif menu_3_selection == '10':
                continue
            elif menu_3_selection == '11':
                continue
            elif menu_3_selection == '12':
                calculator.levermann_12()
            elif menu_3_selection == '13':
                calculator.levermann_13()
            elif menu_3_selection == 'a':
                calculator.levermann_01()
                calculator.levermann_02()
                calculator.levermann_03()
                calculator.levermann_04_05()
                calculator.levermann_06()
                calculator.levermann_07()
                calculator.levermann_08()
                calculator.levermann_09_10_11()
                calculator.levermann_12()
                calculator.levermann_13()
            elif menu_3_selection == 'u':
                menu_3 = False
            elif menu_3_selection == 'x':
                menu_3 = False
                root_menu = False

    elif menu_selection == '4':
        menu_4 = True
        while menu_4:
            print('Sub Menu 3: Show Results')
            print('#(1) Show Stocks sorted by Levermann Score (Top10)')
            print('#(2) ')
            print('------------------------')
            print('(a) Run All')
            print('(u) Up')
            print('(x) Exit')
            menu_4_selection = str(input('> '))
            if menu_4_selection == '1':
                displayer.display_top_10()
            elif menu_4_selection == '2':
                pass
            elif menu_4_selection == 'u':
                menu_4 = False
            elif menu_4_selection == 'x':
                menu_4 = False
                root_menu = False

    elif menu_selection == 'x':
        root_menu = False
