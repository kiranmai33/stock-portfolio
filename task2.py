import yfinance as yf
import json

class StockPortfolio:
    def __init__(self):
        self.portfolio = {}
    
    def add_stock(self, symbol, shares):
        if symbol in self.portfolio:
            self.portfolio[symbol] += shares
        else:
            self.portfolio[symbol] = shares
    
    def remove_stock(self, symbol, shares):
        if symbol in self.portfolio:
            if shares >= self.portfolio[symbol]:
                del self.portfolio[symbol]
            else:
                self.portfolio[symbol] -= shares
    
    def get_portfolio_value(self):
        total_value = 0.0
        for symbol, shares in self.portfolio.items():
            stock = yf.Ticker(symbol)
            current_price = stock.history(period="1d")['Close'].iloc[-1]
            total_value += shares * current_price
        return total_value
    
    def get_portfolio_performance(self):
        performance = {}
        for symbol, shares in self.portfolio.items():
            stock = yf.Ticker(symbol)
            history = stock.history(period="1d")
            current_price = history['Close'].iloc[-1]
            performance[symbol] = {
                "shares": shares,
                "current_price": current_price,
                "total_value": shares * current_price
            }
        return performance

    def save_portfolio(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.portfolio, f)
    
    def load_portfolio(self, filename):
        try:
            with open(filename, 'r') as f:
                self.portfolio = json.load(f)
        except FileNotFoundError:
            print("No saved portfolio found.")

# Main function to demonstrate usage
def main():
    portfolio = StockPortfolio()
    portfolio.load_portfolio('portfolio.json')
    
    while True:
        print("\n1. Add Stock")
        print("2. Remove Stock")
        print("3. View Portfolio Value")
        print("4. View Portfolio Performance")
        print("5. Save Portfolio")
        print("6. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            symbol = input("Enter stock symbol: ").upper()
            shares = int(input("Enter number of shares: "))
            portfolio.add_stock(symbol, shares)
        elif choice == '2':
            symbol = input("Enter stock symbol: ").upper()
            shares = int(input("Enter number of shares to remove: "))
            portfolio.remove_stock(symbol, shares)
        elif choice == '3':
            value = portfolio.get_portfolio_value()
            print(f"Total Portfolio Value: ${value:.2f}")
        elif choice == '4':
            performance = portfolio.get_portfolio_performance()
            for symbol, data in performance.items():
                print(f"{symbol}: {data['shares']} shares @ ${data['current_price']:.2f} = ${data['total_value']:.2f}")
        elif choice == '5':
            portfolio.save_portfolio('portfolio.json')
            print("Portfolio saved.")
        elif choice == '6':
            portfolio.save_portfolio('portfolio.json')
            print("Portfolio saved. Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
