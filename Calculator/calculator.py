from utils import constants as cst
from utils import db_op as db
from utils import date_op as date
from loguru import logger


def levermann_01():
    stock_list = db.get_list(table=cst.TABLE_STOCKS, columns=cst.COLUMN_URI)
    for stock in stock_list:

        # earnings_before_tax = db.get_earnings_after_tax(stock)
        earnings_before_tax = db.get_item(
            table=cst.TABLE_COMPANY_DATA,
            column=cst.COLUMN_EARNINGS_AT,
            condition=[cst.COLUMN_STOCK_URI, stock],
            order=[cst.COLUMN_DATE, cst.DESC],
        )

        # equity_capital = db.get_equity_capital(stock)
        equity_capital = db.get_item(
            table=cst.TABLE_COMPANY_DATA,
            column=cst.COLUMN_EQUITY_CAPITAL,
            condition=[cst.COLUMN_STOCK_URI, stock],
            order=[cst.COLUMN_DATE, cst.DESC],
        )

        if earnings_before_tax is None or equity_capital is None or equity_capital == 0:
            logger.info(
                "Calculate Lev01: Earnings before Tax or Equity Capital is None for stock: %s"
                % stock
            )
            continue

        return_on_equity = round(earnings_before_tax / equity_capital, 2)

        if return_on_equity > 0.2:
            lev_01_score = 1
        elif return_on_equity < 0.1:
            lev_01_score = -1
        else:
            lev_01_score = 0

        # db.save_roe_to_db(stock, return_on_equity, lev_01_score)
        db.upsert_item(
            table=cst.TABLE_LEVERMANN,
            primary_keys=[cst.COLUMN_STOCK_URI, cst.COLUMN_DATE],
            current_date=date.get_current_date(),
            stock_uri=stock,
            lev_01_val=return_on_equity,
            lev_01_sco=lev_01_score,
        )


def levermann_02():
    stock_list = db.get_list(table=cst.TABLE_STOCKS, columns=cst.COLUMN_URI)
    for stock in stock_list:

        # operative_result = db.get_operative_result(stock)
        operative_result = db.get_item(
            table=cst.TABLE_COMPANY_DATA,
            column=cst.COLUMN_OPERATIVE_RESULT,
            condition=[cst.COLUMN_STOCK_URI, stock],
            order=[cst.COLUMN_DATE, cst.DESC],
        )

        # sales_revenue = db.get_sales_revenue(stock)
        sales_revenue = db.get_item(
            table=cst.TABLE_COMPANY_DATA,
            column=cst.COLUMN_SALES_REVENUE,
            condition=[cst.COLUMN_STOCK_URI, stock],
            order=[cst.COLUMN_DATE, cst.DESC],
        )

        if operative_result is None or sales_revenue is None or sales_revenue == 0:
            logger.info(
                "Calculate Lev02: Operative Result or Sales Revenue is None for stock: %s"
                % stock
            )
            continue

        ebit = round(operative_result / sales_revenue, 2)

        if db.check_is_financial_company(stock):
            logger.info("Calculate Lev02: %s is financial Stock" % stock)
            ebit = 0
            lev_02_score = 0
        else:
            if ebit > 0.12:
                lev_02_score = 1
            elif ebit < 0.06:
                lev_02_score = -1
            else:
                lev_02_score = 0

        # db.save_ebit_to_db(stock, ebit, lev_02_score)
        db.upsert_item(
            table=cst.TABLE_LEVERMANN,
            primary_keys=[cst.COLUMN_STOCK_URI, cst.COLUMN_DATE],
            current_date=date.get_current_date(),
            stock_uri=stock,
            lev_02_val=ebit,
            lev_02_sco=lev_02_score,
        )


def levermann_03():
    stock_list = db.get_list(table=cst.TABLE_STOCKS, columns=cst.COLUMN_URI)
    for stock in stock_list:

        # equity_capital = db.get_equity_capital(stock)
        equity_capital = db.get_item(
            table=cst.TABLE_COMPANY_DATA,
            column=cst.COLUMN_EQUITY_CAPITAL,
            condition=[cst.COLUMN_STOCK_URI, stock],
            order=[cst.COLUMN_DATE, cst.DESC],
        )

        # balance = db.get_balance(stock)
        balance = db.get_item(
            table=cst.TABLE_COMPANY_DATA,
            column=cst.COLUMN_BALANCE,
            condition=[cst.COLUMN_STOCK_URI, stock],
            order=[cst.COLUMN_DATE, cst.DESC],
        )

        if equity_capital is None or balance is None or balance == 0:
            logger.info(
                "Calculate Lev03: Equity Capital or Balance is None or 0 for stock: %s"
                % stock
            )
            continue

        equity_ratio = round(equity_capital / balance, 2)

        if db.check_is_financial_company(stock):
            if equity_ratio > 0.10:
                lev_03_score = 1
            elif equity_ratio < 0.05:
                lev_03_score = -1
            else:
                lev_03_score = 0
        else:
            if equity_ratio > 0.25:
                lev_03_score = 1
            elif equity_ratio < 0.15:
                lev_03_score = -1
            else:
                lev_03_score = 0

        # db.save_equity_ratio_to_db(stock, equity_ratio, lev_03_score)
        db.upsert_item(
            table=cst.TABLE_LEVERMANN,
            primary_keys=[cst.COLUMN_STOCK_URI, cst.COLUMN_DATE],
            current_date=date.get_current_date(),
            stock_uri=stock,
            lev_03_val=equity_ratio,
            lev_03_sco=lev_03_score,
        )


def levermann_04_05():
    stock_list = db.get_list(table=cst.TABLE_STOCKS, columns=cst.COLUMN_URI)
    for stock in stock_list:

        # current_stock_price = db.get_latest_stock_price(stock)
        current_stock_price = db.get_item(
            table=cst.TABLE_STOCKS_HISTORIES,
            column=cst.COLUMN_CLOSING_VALUE,
            condition=[cst.COLUMN_STOCK_URI, stock],
            order=[cst.COLUMN_DATE, cst.DESC],
        )
        eps = db.get_current_eps(stock)

        if current_stock_price is None or eps is None:
            logger.info(
                "Calculate Lev04/05: Current Stockprice or EPS is None for stock: %s"
                % stock
            )
            continue

        eps_0 = eps[3]

        kgv5 = current_stock_price / (sum(eps) / 5) if sum(eps) != 0 else 9999.99
        kgv5 = 9999.99 if kgv5 > 9999.99 else kgv5

        kgv0 = current_stock_price / eps_0 if eps_0 != 0 else 14
        kgv0 = 9999.99 if kgv0 > 9999.99 else kgv0

        if 0 < kgv5 < 12:
            lev_04_score = 1
        elif 12 < kgv5 < 16:
            lev_04_score = 0
        elif kgv5 <= 0 or kgv5 >= 16:
            lev_04_score = -1
        else:
            lev_04_score = 0

        # db.save_kgv5_to_db(stock, round(kgv5, 2), lev_04_score)
        db.upsert_item(
            table=cst.TABLE_LEVERMANN,
            primary_keys=[cst.COLUMN_STOCK_URI, cst.COLUMN_DATE],
            current_date=date.get_current_date(),
            stock_uri=stock,
            lev_04_val=round(kgv5, 2),
            lev_04_sco=lev_04_score,
        )

        if 0 < kgv0 < 12:
            lev_05_score = 1
        elif 12 < kgv0 < 16:
            lev_05_score = 0
        elif kgv0 <= 0 or kgv0 >= 16:
            lev_05_score = -1
        else:
            lev_05_score = 0

        # db.save_kgv0_to_db(stock, round(kgv0, 2), lev_05_score)
        db.upsert_item(
            table=cst.TABLE_LEVERMANN,
            primary_keys=[cst.COLUMN_STOCK_URI, cst.COLUMN_DATE],
            current_date=date.get_current_date(),
            stock_uri=stock,
            lev_05_val=round(kgv0, 2),
            lev_05_sco=lev_05_score,
        )


def levermann_06():
    stock_list = db.get_list(table=cst.TABLE_STOCKS, columns=cst.COLUMN_URI)
    for stock in stock_list:
        ratings = db.get_analyst_ratings(stock)
        if ratings is None:
            logger.info("Calculate Lev06: Rating is None for stock: %s" % stock)
            continue
        rating_count = sum(ratings)

        if rating_count == 0:
            logger.info("Calculate Lev06: Zero Rating for stock: %s" % stock)
            rating = 0
            lev_06_score = 0
        else:
            rating = (1 * ratings[0] + 2 * ratings[1] + 3 * ratings[2]) / rating_count
            is_small_cap = db.is_small_cap(stock)

            if is_small_cap and 0 < rating_count <= 5 and 1.0 <= rating <= 1.5:
                lev_06_score = 1
            elif is_small_cap and 0 < rating_count <= 5 and 1.5 < rating < 2.5:
                lev_06_score = 0
            elif is_small_cap and 0 < rating_count <= 5 and 2.5 <= rating <= 3.0:
                lev_06_score = -1

            elif 1.0 <= rating <= 1.5:
                lev_06_score = -1
            elif 1.5 < rating < 2.5:
                lev_06_score = 0
            elif 2.5 <= rating <= 3.0:
                lev_06_score = 1

            else:
                lev_06_score = 5

        # db.save_rating_to_db(stock, round(rating, 2), lev_06_score)
        db.upsert_item(
            table=cst.TABLE_LEVERMANN,
            primary_keys=[cst.COLUMN_STOCK_URI, cst.COLUMN_DATE],
            current_date=date.get_current_date(),
            stock_uri=stock,
            lev_05_val=round(rating, 2),
            lev_05_sco=lev_06_score,
        )


def levermann_07():
    stock_list = db.get_list(table=cst.TABLE_STOCKS, columns=cst.COLUMN_URI)
    for stock in stock_list:
        logger.info("Calculating Lev07 for %s" % stock)
        quarterly_date = db.get_quarterly_date(stock)

        if quarterly_date is None:
            logger.info("Calculate Lev07: Quaterly Date is None for stock: %s" % stock)
            db.save_quarterly_reaction_to_db(stock, 0, 0)
            continue

        index = db.get_main_index_of_stock(stock)
        if index is None:
            logger.info("Calculate Lev07: No Index found")
            continue

        quarterly_stock_pack = db.get_closing_stock_price(quarterly_date, stock)
        quarterly_index_pack = db.get_closing_index_price(quarterly_date, index)
        if quarterly_stock_pack is None or quarterly_index_pack is None:
            logger.info(
                "Calculate Lev07: Quaterly Date Pack or Quaterly Index Pack is None for stock: %s"
                % stock
            )
            continue

        quarterly_stock_closing_price, quarterly_stock_actual_date = (
            quarterly_stock_pack
        )
        quarterly_index_closing_price, quarterly_index_actual_date = (
            quarterly_index_pack
        )

        day_before_actual_date_stock = date.edit_date(
            quarterly_stock_actual_date, cst.DT_MINUS, 1, cst.DT_DAY
        )
        day_before_actual_date_index = date.edit_date(
            quarterly_index_actual_date, cst.DT_MINUS, 1, cst.DT_DAY
        )

        compare_price_stock = db.get_closing_stock_price(
            day_before_actual_date_stock, stock
        )[0]
        compare_price_index = db.get_closing_index_price(
            day_before_actual_date_index, index
        )[0]

        if (
            compare_price_stock is None
            or compare_price_index == 0
            or compare_price_index is None
            or compare_price_index == 0
        ):
            logger.info(
                "Calculate Lev07: Compare Price Stock or Index is None or 0 for stock: %s"
                % stock
            )
            continue
        stock_diff = (quarterly_stock_closing_price / compare_price_stock) - 1
        index_diff = (quarterly_index_closing_price / compare_price_index) - 1

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
    stock_list = db.get_list(table=cst.TABLE_STOCKS, columns=cst.COLUMN_URI)
    for stock in stock_list:
        eps_current = db.get_current_eps(stock)
        eps_last = db.get_last_eps(stock)

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

        db.save_eps_revision_to_db(
            stock, round((eps_0_ratio + eps_1_ratio) / 2, 2), lev_score
        )


def levermann_09_10_11():
    stock_list = db.get_list(table=cst.TABLE_STOCKS, columns=cst.COLUMN_URI)
    for stock in stock_list:
        current_date = date.get_current_date()
        date_minus_6_month = date.edit_date(current_date, cst.DT_MINUS, 6, cst.DT_MONTH)
        date_minus_12_month = date.edit_date(
            current_date, cst.DT_MINUS, 12, cst.DT_MONTH
        )

        current_price_pack = db.get_closing_stock_price(current_date, stock)
        price_6_month_ago_pack = db.get_closing_stock_price(date_minus_6_month, stock)
        price_12_month_ago_pack = db.get_closing_stock_price(date_minus_12_month, stock)

        if (
            current_price_pack is None
            or price_6_month_ago_pack is None
            or price_12_month_ago_pack is None
        ):
            logger.info(
                "Calculate Lev09-11: Current Price or Price before 6M or 12M is None for stock: %s"
                % stock
            )
            continue

        current_price = current_price_pack[0]
        price_6_month_ago = price_6_month_ago_pack[0]
        price_12_month_ago = price_12_month_ago_pack[0]

        if current_price is None:
            logger.info(
                "Calculate Lev09-11: Current Price is None for stock: %s" % stock
            )
            continue

        if (
            price_6_month_ago == 0
            or price_12_month_ago == 0
            or price_6_month_ago is None
            or price_12_month_ago is None
        ):
            logger.info(
                "Calculate Lev09-11:  Price before 6M or 12M is 0 for stock: %s" % stock
            )
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
    stock_list = db.get_list(table=cst.TABLE_STOCKS, columns=cst.COLUMN_URI)
    for stock in stock_list:
        if db.is_small_cap(stock):
            db.save_reversal_to_db(stock, 0, 0)
            continue

        try:
            last_days_of_month = date.get_last_days_of_last_four_months(
                date.get_current_date()
            )
            last_stock_prices_of_month = [
                db.get_closing_stock_price(r_date, stock)[0]
                for r_date in last_days_of_month
            ]

            index = db.get_main_index_of_stock(stock)
            if index is None:
                logger.info("Calculate Lev12: No Index found")
                continue

            last_index_prices_of_month = [
                db.get_closing_index_price(r_date, index)[0]
                for r_date in last_days_of_month
            ]

            stock_changes = db.calculate_list_changes(last_stock_prices_of_month)
            index_changes = db.calculate_list_changes(last_index_prices_of_month)

            differences = []
            for i in range(len(stock_changes)):
                differences.append(stock_changes[i] - index_changes[i])

            avg_diff = round(sum(differences) / 3, 2)

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
    stock_list = db.get_list(table=cst.TABLE_STOCKS, columns=cst.COLUMN_URI)
    for stock in stock_list:
        eps = db.get_current_eps(stock)
        if eps is None:
            logger.info("Calculate Lev13: EPS is None for stock: %s" % stock)
            continue
        if eps[3] != 0:
            eps_ratio = round((eps[4] / eps[3]) - 1, 2)
        else:
            eps_ratio = 0

        if eps_ratio > 0.05:
            lev_score_12 = 1
        elif eps_ratio < -0.05:
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
