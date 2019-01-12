from utils import constants as CST
from utils import db_op as db
from utils import date_op as date
from loguru import logger


def levermann_01():
    stock_list = db.get_stock_names()
    for stock in stock_list:
        earnings_before_tax = db.get_earnings_after_tax(stock)
        equity_capital = db.get_equity_capital(stock)
        if earnings_before_tax is None or equity_capital is None or equity_capital == 0:
            logger.info("Calculate Lev01: Earnings before Tax or Equity Capital is None for stock: %s" % stock)
            continue

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
    for stock in stock_list:
        operative_result = db.get_operative_result(stock)
        sales_revenue = db.get_sales_revenue(stock)

        if operative_result is None or sales_revenue is None:
            logger.info("Calculate Lev02: Operative Result or Sales Revenue is None for stock: %s" % stock)
            continue

        ebit = round(operative_result / sales_revenue, 2)

        if db.check_is_financial_company(stock):
            logger.info("Calculate Lev02: %s is financial Stock" % stock)
            db.save_ebit_to_db(stock, 0, 0)
            continue

        if ebit > 0.12:
            lev_value = 1
        elif ebit < 0.06:
            lev_value = -1
        else:
            lev_value = 0
        db.save_ebit_to_db(stock, ebit, lev_value)


def levermann_03():
    stock_list = db.get_stock_names()
    for stock in stock_list:
        equity_capital = db.get_equity_capital(stock)
        balance = db.get_balance(stock)

        if equity_capital is None or balance is None or balance == 0:
            logger.info("Calculate Lev03: Equity Capital or Balance is None or 0 for stock: %s" % stock)
            continue

        equity_ratio = round(equity_capital / balance, 2)

        if db.check_is_financial_company(stock):
            if equity_ratio > 0.10:
                lev_value = 1
            elif equity_ratio < 0.05:
                lev_value = -1
            else:
                lev_value = 0
            db.save_equity_ratio_to_db(stock, equity_ratio, lev_value)
            continue

        if equity_ratio > 0.25:
            lev_value = 1
        elif equity_ratio < 0.15:
            lev_value = -1
        else:
            lev_value = 0
        db.save_equity_ratio_to_db(stock, equity_ratio, lev_value)


def levermann_04_05():
    stock_list = db.get_stock_names()
    for stock in stock_list:
        current_stock_price = db.get_latest_stock_price(stock)
        eps = db.get_eps(stock)

        if current_stock_price is None or eps is None:
            logger.info("Calculate Lev04/05: Current Stockprice or EPS is None for stock: %s" % stock)
            continue

        eps_0 = eps[3]

        if sum(eps) != 0:
            kgv5 = current_stock_price/(sum(eps)/5)
        else:
            kgv5 = 9999.99

        if kgv5 > 9999.99:
            kgv5 = 9999.99

        if eps_0 != 0:
            kgv0 = current_stock_price/eps_0
        else:
            kgv0 = 14

        if 0 < kgv5 < 12:
            kgv5_score = 1
        elif 12 < kgv5 < 16:
            kgv5_score = 0
        elif kgv5 <= 0 or kgv5 >= 16:
            kgv5_score = -1
        else:
            kgv5_score = 0

        db.save_kgv5_to_db(stock, round(kgv5, 2), kgv5_score)

        if kgv0 > 9999.99:
            kgv0 = 9999.99

        if 0 < kgv0 < 12:
            kgv0_score = 1
        elif 12 < kgv0 < 16:
            kgv0_score = 0
        elif kgv0 <= 0 or kgv0 >= 16:
            kgv0_score = -1
        else:
            kgv0_score = 0

        db.save_kgv0_to_db(stock, round(kgv0, 2), kgv0_score)


def levermann_06():
    stock_list = db.get_stock_names()
    for stock in stock_list:
        ratings = db.get_analyst_ratings(stock)
        rating_count = sum(ratings)

        if rating_count == 0:
            logger.info("Calculate Lev06: Zero Rating for stock: %s" % stock)
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
    for stock in stock_list:

        quaterly_date = db.get_quarterly_date(stock)

        if quaterly_date is None:
            logger.info("Calculate Lev07: Quaterly Date is None for stock: %s" % stock)
            db.save_quarterly_reaction_to_db(stock, 0, 0)
            continue

        index = db.get_index_of_stock(stock)

        quaterly_stock_pack = db.get_closing_stock_price(quaterly_date, stock)
        quaterly_index_pack = db.get_closing_index_price(quaterly_date, index)
        if quaterly_stock_pack is None or quaterly_index_pack is None:
            logger.info("Calculate Lev07: Quaterly Date Pack or Quaterly Index Pack is None for stock: %s" % stock)
            continue

        quaterly_stock_closing_price, quarterly_stock_actual_date = quaterly_stock_pack
        quaterly_index_closing_price, quarterly_index_actual_date = quaterly_index_pack

        day_before_actual_date_stock = date.edit_date(quarterly_stock_actual_date, CST.DT_MINUS, 1, CST.DT_DAY)
        day_before_actual_date_index = date.edit_date(quarterly_index_actual_date, CST.DT_MINUS, 1, CST.DT_DAY)

        compare_price_stock = db.get_closing_stock_price(day_before_actual_date_stock, stock)[0]
        compare_price_index = db.get_closing_index_price(day_before_actual_date_index, index)[0]

        if compare_price_stock is None or compare_price_index == 0 \
                or compare_price_index is None or compare_price_index == 0:
            logger.info("Calculate Lev07: Compare Price Stock or Index is None or 0 for stock: %s" % stock)
            continue
        stock_diff = (quaterly_stock_closing_price / compare_price_stock) - 1
        index_diff = (quaterly_index_closing_price / compare_price_index) - 1

        if index_diff == 0:
            continue
        combined_diff = round(stock_diff - index_diff, 2)

        if combined_diff >= 0.01:
            lev_score = 1
        elif -0.01 < combined_diff < 0.01:
            lev_score = 0
        elif combined_diff <= -0.01:
            lev_score = -1

        db.save_quarterly_reaction_to_db(stock, combined_diff, lev_score)


def levermann_08():
    stock_list = db.get_stock_names()
    for stock in stock_list:
        eps_current = db.get_eps(stock)
        eps_last = db.get_older_eps(stock)

        if eps_current is None:
            logger.info("Calculate Lev08: Current EPS is None for stock: %s" % stock)
            continue

        if eps_last is None:
            logger.info("Calculate Lev08: Last EPS is None for stock: %s" % stock)
            db.save_eps_revision_to_db(stock, 0, 0)
            continue

        eps_0_c = eps_current[3]
        eps_1_c = eps_current[4]

        eps_0_l = eps_last[3]
        eps_1_l = eps_last[4]

        if eps_0_l == 0 or eps_1_l == 0:
            continue

        eps_0_ratio = (eps_0_c / eps_0_l) - 1
        eps_1_ratio = (eps_1_c / eps_1_l) - 1

        if eps_0_ratio > 0.05 or eps_1_ratio > 0.05:
            lev_score = 1
        elif eps_0_ratio < -0.05 or eps_1_ratio < -0.05:
            lev_score = -1
        else:
            lev_score = 0

        db.save_eps_revision_to_db(stock, round((eps_0_ratio+eps_1_ratio)/2, 2), lev_score)


def levermann_09_10_11():
    stock_list = db.get_stock_names()
    for stock in stock_list:
        current_date = date.get_current_date()
        date_minus_6_month = date.edit_date(current_date, CST.DT_MINUS, 6, CST.DT_MONTH)
        date_minus_12_month = date.edit_date(current_date, CST.DT_MINUS, 12, CST.DT_MONTH)

        current_price_pack = db.get_closing_stock_price(current_date, stock)
        price_6_month_ago_pack = db.get_closing_stock_price(date_minus_6_month, stock)
        price_12_month_ago_pack = db.get_closing_stock_price(date_minus_12_month, stock)

        if current_price_pack is None or price_6_month_ago_pack is None or price_12_month_ago_pack is None:
            logger.info("Calculate Lev09-11: Current Price or Price before 6M or 12M is None for stock: %s" % stock)
            continue

        current_price = current_price_pack[0]
        price_6_month_ago = price_6_month_ago_pack[0]
        price_12_month_ago = price_12_month_ago_pack[0]

        if price_6_month_ago == 0 or price_12_month_ago == 0:
            logger.info("Calculate Lev09-11:  Price before 6M or 12M is 0 for stock: %s" % stock)
            continue

        ratio_6_month = round((current_price / price_6_month_ago) - 1, 2)
        ratio_12_month = round((current_price / price_12_month_ago) - 1, 2)

        if ratio_6_month > 0.05:
            lev_score_09 = 1
        elif ratio_6_month < -0.05:
            lev_score_09 = -1
        else:
            lev_score_09 = 0

        db.save_6_months_ratio_to_db(stock, ratio_6_month, lev_score_09)

        if ratio_12_month > 0.05:
            lev_score_10 = 1
        elif ratio_12_month < -0.05:
            lev_score_10 = -1
        else:
            lev_score_10 = 0

        db.save_12_months_ratio_to_db(stock, ratio_12_month, lev_score_10)

        if lev_score_09 == 1 and lev_score_10 <= 0:
            lev_score_11 = 1
        elif lev_score_09 == -1 and lev_score_10 >= 0:
            lev_score_11 = -1
        else:
            lev_score_11 = 0

        db.save_momentum_to_db(stock, lev_score_11)


def levermann_12():
    stock_list = db.get_stock_names()
    for stock in stock_list:
        if db.is_small_cap(stock):
            db.save_reversal_to_db(stock, 0, 0)
            continue

        try:
            last_days_of_month = date.get_last_days_of_last_four_months()
            last_stock_prices_of_month = [db.get_closing_stock_price(r_date, stock)[0] for r_date in last_days_of_month]

            index = db.get_index_of_stock(stock)
            last_index_prices_of_month = [db.get_closing_index_price(r_date, index)[0] for r_date in last_days_of_month]

            stock_changes = db.calculate_list_changes(last_stock_prices_of_month)
            index_changes = db.calculate_list_changes(last_index_prices_of_month)

            differences = []
            for i in range(len(stock_changes)):
                differences.append(stock_changes[i]-index_changes[i])

            avg_diff = round(sum(differences)/3, 2)

            if all(i > 0 for i in differences):
                lev_score_12 = -1
            elif all(i < 0 for i in differences):
                lev_score_12 = 1
            else:
                lev_score_12 = 0

            db.save_reversal_to_db(stock, avg_diff, lev_score_12)
        except TypeError:
            logger.exception("Calculate Lev12 TypeError at stock: %s" % stock)
            continue


def levermann_13():
    stock_list = db.get_stock_names()
    for stock in stock_list:
        eps = db.get_eps(stock)
        if eps is None:
            logger.info("Calculate Lev13: EPS is None for stock: %s" % stock)
            continue
        if eps[3] != 0:
            eps_ratio = round((eps[4] / eps[3]) - 1, 2)
        else:
            eps_ratio = 0

        if eps_ratio > 0.05:
            lev_score_12 = 1
        elif eps_ratio > -0.05:
            lev_score_12 = -1
        else:
            lev_score_12 = 0

        db.save_profit_growth_to_db(stock, eps_ratio, lev_score_12)


def run_all():
    levermann_01()
    levermann_02()
    levermann_03()
    levermann_04_05()
    levermann_06()
    levermann_07()
    levermann_08()
    levermann_09_10_11()
    levermann_12()
    levermann_13()
