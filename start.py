from Scraper import scraper
from Parser import parser


root_menu = True

while root_menu:
    print('Main Menu')
    print('(1) Scraping')
    print('(2) Parsing')
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
            print('(4) Scrap Stock Overview')
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
                scraper.scrap_stock_overview()
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
            print('(3) Write Stock Histories to DB')
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
            elif menu_2_selection == 'u':
                menu_2 = False
            elif menu_2_selection == 'x':
                menu_2 = False
                root_menu = False

    elif menu_selection == 'x':
        root_menu = False