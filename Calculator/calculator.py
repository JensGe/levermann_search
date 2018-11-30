from utils import constants as CST
from utils import db_op as db


def levermann_01():
    stock_list = db.get_stock_names()
    for stock in stock_list[:10]: #TODO delete :10 Limit
        earnings_before_tax = db.get_earnings_after_tax(stock)
        equity_capital = db.get_equity_capital(stock)
        return_on_equity = round(earnings_before_tax / equity_capital, 2)
        if return_on_equity > 0.2:
            lev_value = 1
        elif return_on_equity < 0.1:
            lev_value = -1
        else:
            lev_value = 0
        db.save_roe_to_db(stock, return_on_equity, lev_value)


def levermann_02():
    stock_list = db.get_stock_names()
    for stock in stock_list[:10]: #TODO delete :10 Limit
        operative_result = db.get_operative_result(stock)
        sales_revenue = db.get_sales_revenue(stock)
        ebit = round(operative_result / sales_revenue, 2)
        # ToDo Check for Finance Company
        if ebit > 0.12:
            lev_value = 1
        elif ebit < 0.06:
            lev_value = -1
        else:
            lev_value = 0
        db.save_ebit_to_db(stock, ebit, lev_value)


def levermann_03():
    stock_list = db.get_stock_names()
    for stock in stock_list[:10]: #TODO delete :10 Limit
        equity_capital = db.get_equity_capital(stock)
        balance = db.get_balance(stock)
        equity_ratio = round(equity_capital / balance, 2)
        # ToDo Check for Finance Company
        if equity_ratio > 0.25:
            lev_value = 1
        elif equity_ratio < 0.15:
            lev_value = -1
        else:
            lev_value = 0
        db.save_equity_ratio_to_db(stock, equity_ratio, lev_value)


def levermann_04_05():
    stock_list = db.get_stock_names()
    for stock in stock_list[:10]: #TODO delete :10 Limit
        current_stock_price = db.get_current_stock_price(stock)
        eps = db.get_eps(stock)

        kgv5 = round(current_stock_price/(sum(eps)/5), 2)
        kgv0 = round(current_stock_price/eps[3], 2)
        if 0 < kgv5 < 0.12:
            kgv5_score = 1
        elif 12 < kgv5 < 0.16:
            kgv5_score = 0
        elif kgv5 <= 0 or kgv5 >= 16:
            kgv5_score = -1
        else:
            kgv5_score = 0

        if 0 < kgv0 < 0.12:
            kgv0_score = 1
        elif 12 < kgv0 < 0.16:
            kgv0_score = 0
        elif kgv0 <= 0 or kgv0 >= 16:
            kgv0_score = -1
        else:
            kgv0_score = 0
        db.save_kgv5_to_db(stock, kgv5, kgv5_score)
        db.save_kgv0_to_db(stock, kgv0, kgv0_score)


def levermann_06():
    stock_list = db.get_stock_names()
    for stock in stock_list[:10]: #TODO delete :10 Limit
        ratings = db.get_analyst_ratings(stock)
        rating_count = sum(ratings)

        if rating_count == 0:
            db.save_rating_to_db(stock, 0, 0)
            continue

        rating = round((1 * ratings[0] + 2 * ratings[1] + 3 * ratings[2]) / rating_count, 2)
        is_small_cap = db.is_small_cap(stock)

        if is_small_cap and 0 < rating_count <= 5 and 1.0 <= rating <= 1.5:
            rating_score = 1
        elif is_small_cap and 0 < rating_count <= 5 and 1.5 < rating < 2.5:
            rating_score = 0
        elif is_small_cap and 0 < rating_count <= 5 and 2.5 <= rating <= 3.0:
            rating_score = -1

        elif 1.0 <= rating <= 1.5:
            rating_score = -1
        elif 1.5 < rating < 2.5:
            rating_score = 0
        elif 2.5 <= rating <= 3.0:
            rating_score = 1

        else:
            rating_score = 5

        db.save_rating_to_db(stock, rating, rating_score)


def levermann_07():
    stock_list = db.get_stock_names()
    for stock in stock_list[:10]: #TODO delete :10 Limit
        quaterly_date = db.get_quarterly_date(stock)

        if quaterly_date is None:
            db.save_quaterly_reaction_to_db(stock, 0, 0)
            continue

        quaterly_stock_closing_price = db.get_closing_stock_price(quaterly_date, stock)
        index = db.get_index_of_stock(stock)
        quaterly_index_closing_price = db.get_closing_index_price(quaterly_date, index)



        ratio = 0


        if ratio > 0.01:
            lev_score = 1
        elif -0.01 < ratio < 0.01:
            lev_score = 0
        elif ratio < -0.01:
            lev_score = -1


        db.save_rating_to_db(stock, ratio, lev_score)