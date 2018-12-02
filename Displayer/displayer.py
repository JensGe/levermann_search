from utils import db_op as db


def display_top_10():
    results = db.get_levermann_full_table()
    for item in results:
        print("%s: \t%s" % (item['AktienURI'], str(item['ScoreSum'])))