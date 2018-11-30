from Scraper import scraper
from Parser import parser
from Calculator import calculator


root_menu = True

while root_menu:
    print('Main Menu')
    print('(1) Scraping')
    print('(2) Parsing')
    print('(3) Calculate')
    print('---------------')
    print('(x) Exit')

    menu_selection = str(input('> '))

    if menu_selection == '1':
        menu_1 = True
        while menu_1:
            print('Sub Menu 1: Scraping')
            print('(1) Scrap Index Contents')
            print('(2) Scrap Index Histories')
            print('------------------------')
            print('(3) Scrap Stock Histories')
            print('(4) Scrap Stock Infos')
            print('------------------------')
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
            elif menu_1_selection == 'u':
                menu_1 = False
            elif menu_1_selection == 'x':
                menu_1 = False
                root_menu = False

    elif menu_selection == '2':
        menu_2 = True
        while menu_2:
            print('Sub Menu 2: Parsing')
            print('(1) Write Index Contents to DB')
            print('(2) Write Index Histories to DB')
            print('------------------------------')
            print('(3) Write Stock Histories to DB')
            print('(4) Write Stock Overview to DB')
            print('(5) Write Stock Balance to DB')
            print('(6) Write Stock Estimates to DB')
            print('(7) Write Stock Targets to DB')
            print('(8) Write Stock Dates to DB')
            print('------------------------------')
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
            elif menu_2_selection == 'u':
                menu_2 = False
            elif menu_2_selection == 'x':
                menu_2 = False
                root_menu = False

    if menu_selection == '3':
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
            print('#(9) Stock Change 6 Month')
            print('#(10) Stock Change 12 Month')
            print('#(11) Stock Momentum')
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
                continue
            elif menu_3_selection == '9':
                continue
            elif menu_3_selection == '10':
                continue
            elif menu_3_selection == '11':
                continue
            elif menu_3_selection == '12':
                continue
            elif menu_3_selection == '13':
                continue
            elif menu_3_selection == 'a':
                continue
            elif menu_3_selection == 'u':
                menu_3 = False
            elif menu_3_selection == 'x':
                menu_3 = False
                root_menu = False

    elif menu_selection == 'x':
        root_menu = False
