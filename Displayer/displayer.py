from utils import db_op as db


def display_levermann_buy():
    results = db.get_levermann_buy()
    for item in results:
        print("%s \t %s \t %s \t %s \t %s" % (item['AktienURI'],
                                              str(item['Datum']),
                                              str(item['ScoreSum']),
                                              str(item['Marktkapitalisierung']),
                                              str(item['Branchen'])))


def display_levermann_hold():
    results = db.get_levermann_hold()
    for item in results:
        print("%s \t %s \t %s \t %s \t %s" % (item['AktienURI'],
                                              str(item['Datum']),
                                              str(item['ScoreSum']),
                                              str(item['Marktkapitalisierung']),
                                              str(item['Branchen'])))

