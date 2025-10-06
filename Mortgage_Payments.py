"""
FINE 3300 A (Fall 2025) - Assignment 1
Part 1: Mortgage Payments

This code creates a MortgagePayment class that computes the payment amount for the requested payment frequencies (monthly, semi-monthly, bi-weekly, weekly, rapid bi-weekly (half the monthly amount), rapid weekly (quarter of the monthly amount)

Key Assumptions:
  - Quoted mortgage rates are compounded semi-annually
  - We convert the quoted nominal rate (which is semi-annual compounding) to an Effective Annual Rate (EAR), then derive periodic rates by dividing EAR by payments-per-year
  - No input validation (per assignment instructions)
"""

# ------------------------------
# Part 1 - Mortgage Payments
# ------------------------------

class MortgagePayment:
    def __init__(self, quoted_rate_percent: float, amortization_years: int):
        #Initialize with quoted annual rate (as a percent, e.g., 5.5) and amortization (years)
        self.__quoted_rate_percent = float(quoted_rate_percent)
        self.__amort_years = int(amortization_years)

    #The following methods are private (indicated by "__") because these are internal and won't be used outside of this
    def __ear_from_semi_annual(self) -> float:
        #Convert the Canadian quoted (semi-annual compounding) nominal rate to EAR
        r_nom = self.__quoted_rate_percent / 100.0  # convert percent to decimal
        ear = (1 + r_nom / 2.0) ** 2 - 1.0
        return ear

    def __annuity_pva(self, r: float, n: int) -> float:
        #Present Value of an Annuity factor: PVA(r, n) = (1 - (1 + r)^-n) / r
        
        #Handles the r=0 case explicitly.
        if r == 0:
            return float(n)
        return (1.0 - (1.0 + r) ** (-n)) / r

    def __level_payment(self, principal: float, payments_per_year: int) -> float:
        #Compute the level payment given a frequency using EAR -> periodic rate
        #Quoted rate (semi-annual)
        rate = self.__quoted_rate_percent / 100.0
        #Per-payment effective rate
        r_periodic = (1.0 + rate / 2.0) ** (2.0 / float(payments_per_year)) - 1.0
        n_periods = int(self.__amort_years * payments_per_year)
        pva = self.__annuity_pva(r_periodic, n_periods)
        return 0.0 if pva == 0 else principal / pva

    def payments(self, principal: float):
        """this part should return the following tuple: (monthly, semi_monthly, bi_weekly, weekly, rapid_bi_weekly, rapid_weekly)
        and rounding is done when printing at the end to use accurate numbers throughout"""
        
        p = float(principal)

        monthly = self.__level_payment(p, 12)
        semi_monthly = self.__level_payment(p, 24)
        bi_weekly = self.__level_payment(p, 26)
        weekly = self.__level_payment(p, 52)

        #Accelerated versions relative to the monthly payment
        rapid_bi_weekly = monthly / 2.0
        rapid_weekly = monthly / 4.0

        return (monthly, semi_monthly, bi_weekly, weekly, rapid_bi_weekly, rapid_weekly)

def _format_currency(x: float) -> str:
    return f"${x:,.2f}"


if __name__ == "__main__":
    print("FINE3300 - Assignment 1 (Part 1: Mortgage Payments)")
    principal = float(input("Enter principal amount ($): ").strip())
    quoted_rate = float(input("Enter quoted annual rate (%): ").strip())
    years = int(input("Enter amortization period (years): ").strip())

    mp = MortgagePayment(quoted_rate, years)
    m, sm, bw, w, rbw, rw = mp.payments(principal)

    print(f"Monthly Payment: {_format_currency(round(m, 2))}")
    print(f"Semi-monthly Payment: {_format_currency(round(sm, 2))}")
    print(f"Bi-weekly Payment: {_format_currency(round(bw, 2))}")
    print(f"Weekly Payment: {_format_currency(round(w, 2))}")
    print(f"Rapid Bi-weekly Payment: {_format_currency(round(rbw, 2))}")
    print(f"Rapid Weekly Payment: {_format_currency(round(rw, 2))}")
