"""Centralized portfolio performance math for dashboard endpoints."""
import pandas as pd


class PortfolioService:
    @staticmethod
    def calc_current_price(avg_price: float, variations: list[dict]) -> float:
        price = avg_price
        for v in variations:
            price = price * (1 + float(v["pct_change"]) / 100)
        return round(price, 4)

    @staticmethod
    def calc_variation_return(invested: float, current_value: float) -> float:
        return 0.0 if invested == 0 else round(((current_value - invested) / invested) * 100, 2)

    @staticmethod
    def calc_dividend_return(dividends_total: float, invested: float) -> float:
        return 0.0 if invested == 0 else round((dividends_total / invested) * 100, 2)

    @staticmethod
    def calc_total_return(var_pct: float, div_pct: float) -> float:
        return round(var_pct + div_pct, 2)

    @staticmethod
    def build_performance_series(variations_df: pd.DataFrame) -> list[dict]:
        if variations_df.empty:
            return []
        df = variations_df.sort_values("date")
        df["daily_weighted"] = df["pct_change"] * df["weight"]
        cumulative = (1 + (df.groupby("date")["daily_weighted"].sum() / 100)).cumprod() - 1
        return [{"date": str(d), "return_pct": round(v * 100, 4)} for d, v in cumulative.items()]
