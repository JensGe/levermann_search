from Scraper import scraper
from Parser import parser


scraper.scrap_index_content_sites()

parser.write_index_contents_from_html_to_db()

