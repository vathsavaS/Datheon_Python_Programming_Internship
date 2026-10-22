
import csv
import os
from datetime import datetime

PRICE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_prices.csv")
SUMMARY_FILE = "portfolio_summary.csv"


def load_prices():
    prices = {}

    with open(PRICE_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            ticker = row["ticker"].strip().upper()
            prices[ticker] = float(row["current_price"])

    return prices


def get_positive_float(message):
    while True:
        try:
            value = float(input(message))

            if value > 0:
                return value

            print("Enter a number greater than zero.")

        except ValueError:
            print("Invalid input. Please enter a number.")


def get_positive_integer(message):
    while True:
        try:
            value = int(input(message))

            if value > 0:
                return value

            print("Enter a whole number greater than zero.")

        except ValueError:
            print("Invalid input. Please enter a whole number.")


def main():
    print("\n=== INVESTMENT PORTFOLIO TRACKER ===")

    if not os.path.exists(PRICE_FILE):
        print("Error: sample_prices.csv was not found.")
        return

    prices = load_prices()
    portfolio = {}

    print("\nAvailable stocks:")
    for ticker, price in prices.items():
        print(f"{ticker}: Rs. {price:.2f}")

    print("\nEnter DONE when you finish adding stocks.")

    while True:
        ticker = input("\nEnter stock ticker: ").strip().upper()

        if ticker == "DONE":
            break

        if ticker not in prices:
            print("Stock not found. Choose a listed ticker.")
            continue

        buy_price = get_positive_float("Enter buy price per share: ")
        quantity = get_positive_integer("Enter number of shares: ")

        # Store the holding in a dictionary
        if ticker in portfolio:
            old = portfolio[ticker]
            old_quantity = old["quantity"]
            new_quantity = old_quantity + quantity

            old["buy_price"] = (
                old["buy_price"] * old_quantity
                + buy_price * quantity
            ) / new_quantity

            old["quantity"] = new_quantity
        else:
            portfolio[ticker] = {
                "buy_price": buy_price,
                "quantity": quantity
            }

        print(f"{ticker} added successfully!")

    if not portfolio:
        print("No stocks entered. Exiting.")
        return

    total_invested = 0
    total_market_value = 0
    timestamp = datetime.now().astimezone().isoformat(
        timespec="seconds"
    )

    print("\n" + "=" * 78)
    print(f"{'TICKER':<12}{'QTY':>6}{'BUY PRICE':>13}"
          f"{'CURRENT':>13}{'VALUE':>13}{'GAIN/LOSS':>13}")
    print("=" * 78)

    rows = []

    for ticker, holding in portfolio.items():
        buy_price = holding["buy_price"]
        quantity = holding["quantity"]
        current_price = prices[ticker]

        invested = buy_price * quantity
        market_value = current_price * quantity
        profit_loss = market_value - invested
        percentage = (profit_loss / invested) * 100

        total_invested += invested
        total_market_value += market_value

        print(
            f"{ticker:<12}{quantity:>6}"
            f"{buy_price:>13.2f}{current_price:>13.2f}"
            f"{market_value:>13.2f}{profit_loss:>13.2f}"
        )
        print(f"  Gain/Loss percentage: {percentage:+.2f}%")

        rows.append({
            "timestamp": timestamp,
            "ticker": ticker,
            "buy_price": f"{buy_price:.2f}",
            "quantity": quantity,
            "current_price": f"{current_price:.2f}",
            "invested_amount": f"{invested:.2f}",
            "market_value": f"{market_value:.2f}",
            "profit_loss": f"{profit_loss:.2f}",
            "gain_loss_percent": f"{percentage:.2f}"
        })

    total_profit_loss = total_market_value - total_invested
    total_percentage = (
        total_profit_loss / total_invested
    ) * 100

    print("=" * 78)
    print(f"Total invested: Rs. {total_invested:.2f}")
    print(f"Current market value: Rs. {total_market_value:.2f}")
    print(
        f"Total gain/loss: Rs. {total_profit_loss:+.2f}"
        f" ({total_percentage:+.2f}%)"
    )

    # Save the portfolio summary to a CSV file
    fields = [
        "timestamp", "ticker", "buy_price", "quantity",
        "current_price", "invested_amount", "market_value",
        "profit_loss", "gain_loss_percent"
    ]

    file_exists = (
        os.path.exists(SUMMARY_FILE)
        and os.path.getsize(SUMMARY_FILE) > 0
    )

    with open(
        SUMMARY_FILE, "a", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fields)

        if not file_exists:
            writer.writeheader()

        writer.writerows(rows)

        writer.writerow({
            "timestamp": timestamp,
            "ticker": "PORTFOLIO_TOTAL",
            "buy_price": "",
            "quantity": "",
            "current_price": "",
            "invested_amount": f"{total_invested:.2f}",
            "market_value": f"{total_market_value:.2f}",
            "profit_loss": f"{total_profit_loss:.2f}",
            "gain_loss_percent": f"{total_percentage:.2f}"
        })

    print(f"\nSummary saved to {SUMMARY_FILE}!")


if __name__ == "__main__":
    main()
