"""
FINE 3300 A (Fall 2025) - Assignment 1
Part 2 - Exchange Rates

This code implements an "ExchangeRates" class that reads the .csv file provided and extracts the latest USD/CAD rate (from the last row) and uses it to complete the users conversion request

Key Assumptions:
  - The CSV column name is "USD/CAD" (like in the original file, any changes will not work with the code)
  - The column value is the USD-to-CAD rate, thus the math is as follows:
      USD -> CAD: amount * rate
      CAD -> USD: amount / rate
"""

import csv

# ------------------------------
# Part 2 - Exchange Rates
# ------------------------------

class ExchangeRates:
    def __init__(self, csv_path: str):
        """Initialize with path to the Bank of Canada Exchange Rate CSV file."""
        self.__csv_path = csv_path
        self.__usd_to_cad = None  # private variable, loaded on demand

    def __find_latest_rate(self):
        """Reads the CSV and stores the most recent USD->CAD rate (last row)."""
        with open(self.__csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            key = "USD/CAD"
            if key not in reader.fieldnames:
                raise ValueError("CSV file does not contain 'USD/CAD' column.")

            last_row = None
            for row in reader:
                last_row = row  # loop to the last line

            if last_row is None:
                raise ValueError("CSV appears to have no data rows.")

            raw_value = last_row.get(key, "").strip()
            if raw_value == "":
                raise ValueError("Latest row has empty USD/CAD value.")

            self.__usd_to_cad = float(raw_value)

    def get_usd_to_cad(self) -> float:
        """Return the latest USD->CAD rate (loads it if needed)."""
        if self.__usd_to_cad is None:
            self.__find_latest_rate()
        return self.__usd_to_cad

    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """Convert amount between CAD and USD using the latest USD/CAD rate.
           - If from_currency == to_currency, returns amount unchanged.
           - USD -> CAD: amount * rate
           - CAD -> USD: amount / rate
        """
        amt = float(amount)
        from_c = from_currency.strip().upper()
        to_c = to_currency.strip().upper()

        if from_c == to_c:
            return amt

        rate = self.get_usd_to_cad()

        if from_c == "USD" and to_c == "CAD":
            return amt * rate
        elif from_c == "CAD" and to_c == "USD":
            return amt / rate
        else:
            raise ValueError("Only USD and CAD conversions are supported by this assignment.")


# ---------- Utility for display ----------
def _format_currency(x: float, code: str) -> str:
    return f"{code} ${x:,.2f}"


# ---------- Script mode (for assignment screenshot) ----------
if __name__ == "__main__":
    print("FINE3300 - Assignment 1 (Part 2: Exchange Rates)")

    amt = float(input("Enter amount (e.g., 100000): ").strip())
    from_ccy = input("From currency (USD or CAD): ").strip().upper()
    to_ccy = input("To currency (USD or CAD): ").strip().upper()

    xr = ExchangeRates("BankOfCanadaExchangeRates.csv")
    result = xr.convert(amt, from_ccy, to_ccy)

    print(f"{_format_currency(amt, from_ccy)} = {_format_currency(result, to_ccy)}")


