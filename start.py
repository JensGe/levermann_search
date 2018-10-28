from Scraper import scraper
from Parser import parser


print('##################################')
print('# (1) Scrap Index Content Sites  #')
print('# (2) Write Index Contents to DB #')
print('#                                #')
print('##################################')

selection = input('# > ')

if selection == '1':
    scraper.scrap_index_content_sites()
elif selection == '2':
    parser.write_index_contents_from_html_to_db()
else:
    quit(0)

