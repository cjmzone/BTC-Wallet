from datetime import datetime
import requests
from bs4 import BeautifulSoup as bs

class Date:
    def __init__(self): 
        self.todays_date = ""
        self.format_date = ""
        self.time = ""
        self.format_time = ""
    
    def getDate(self): 
        self.todays_date = datetime.now()
        self.format_date = self.todays_date.strftime("%d/%m/%Y")
        return self.format_date
    
    def getTime(self):
        self.time = datetime.now()
        self.format_time = self.time.strftime("%H:%M:%S")
        return self.format_time

class GetLive:
    def __init__(self):
        self.headers = ""
        self.BTC_URL = ""
        self.request = ""
        self.soup = ""
        self.price = ""
        self.update_price = ""
        self.float_price = 0.0

    def getPrice(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'}
        self.BTC_URL = "https://coinmarketcap.com/currencies/bitcoin/"
        self.request = requests.get(self.BTC_URL, self.headers)
        self.soup = bs(self.request.content, "html.parser")
        self.price = self.soup.find("div",{"class":"priceValue"})
        return float(self.price.text.replace("$","").replace(",",""))

class Wallet:
    def __init__ (self):
        self.shares = 0
        self.btc = GetLive()
        self.capital = 75000
        self.btcValue = 0
        
    def purchasedBTC(self, capital, shares):
        #float("{:.2f}".format(capital))
        self.capital = float("{:.2f}".format(capital))
        #self.shares = float("{:.2f}".format(self.shares + shares))
        self.shares = self.shares + shares
        return self.capital, self.shares
    
    def soldBTC(self, capital, shares):
        #float("{:.2f}".format(capital))
        self.capital = float("{:.2f}".format(capital))
        self.shares = float("{:.2f}".format(self.shares - shares))
        return self.capital, self.shares
        
    def seeBalance(self,capital,shares):
        print("Current USD amount:", self.capital)
        print("Tokens in wallet:  ", self.shares)
        print("Current BTC price: ", self.btc.getPrice())
        
class Ledger:
    def __init__(self):
        self.transaction = []
        self.wallet = Wallet()
    
    def addTransaction(self,m_transaction):
        self.transaction.append([m_transaction])
        
    def viewTransactions(self):
        print("\nTransaction History:")
        for eachItem in self.transaction:
            print(eachItem)
#main 
def main():
    # Global Variables
    m_wallet = Wallet()
    m_ledger = Ledger()
    date = Date()
    
    def buyBTC(capital, shares):
        
        if(m_wallet.capital <= 0):
            print("Sorry, you're out of money!")
        else:
            print(f"\nYour total USD:                     ${m_wallet.capital}")
            print(f"Your total dollar amount in BTC:    ${m_wallet.btcValue}")
            print(f"Your total amount of BTC tokens:     {m_wallet.shares}")
            print(f"\nCurrent price of 1 BTC token:       ${m_wallet.btc.getPrice()}")
            
            
            while True:
                try:
                    shares = float(input("How many BTC tokens would you like to purchase? "))
                    if (isinstance(shares,str) == True):
                        raise ValueError
                    
                    # update investment and capital
                    btcValue = shares * m_wallet.btc.getPrice()
                    print(f"Purchasing ${btcValue:.2f} in BTC ...")
                    
                    if(btcValue > m_wallet.capital):
                        print("Your purchase amount is greater than your capital. \nPlease try again.")
                    else:
                        m_wallet.btcValue += float("{:.2f}".format(shares * m_wallet.btc.getPrice()))
                        capital = float("{:.2f}".format(capital)) - m_wallet.btcValue
                        # create transaction String
                        transaction = "Purchased " + str(shares) + " shares worth of BTC on " + str(date.getDate()) + " at " + str(date.getTime()) + " valued at " + str(m_wallet.btc.getPrice()) + "."
                        
                        # Update Wallet and Ledger
                        m_wallet.purchasedBTC(capital, shares)
                        m_ledger.addTransaction(transaction)
                        
                        return capital, shares
                except ValueError:
                    print("Your entry must be numerical. Try again...")
                        
            
    def sellBTC(capital, shares):
        print("Current pirce of 1 BTC token:",m_wallet.btc.getPrice())
        shares = float(input("How many BTC tokens would you like to sell? "))
        
        # update investment and capital
        investment = shares * m_wallet.btc.getPrice()
        capital = float("{:.2f}".format(capital)) + investment
        
        # create transaction String
        transaction = "Sold " + str(shares) + " shares worth of BTC on " + str(date.getDate()) + " at " + str(date.getTime()) + " valued at " + str(m_wallet.btc.getPrice()) + "."
        
        # Update Wallet and Ledger
        m_wallet.soldBTC(capital, shares)
        m_ledger.addTransaction(transaction)
        
        return capital, shares
    
    def tradeAgain():
        print()
        while True:
            try:
                play = input(str("Would you like to return to the main menu? (y/n): "))
                if play not in ["y","n"]:
                    raise ValueError
                if(play == "y"):
                    print()
                    menu()
                elif(play == "n"):
                    exit()
                return
            except ValueError:
                print("Invalid input! Try again...")
    
    def menu():
        while True:
            try: 
                choice = int(input("Please select from the following options (1 - 6): \n \n 1) Buy BTC \n 2) Sell BTC \n 3) See your USD Balance \n 4) See BTC Price \n 5) See Buy/Sell History \n 6) Exit \n \n  > "))
                
                if(choice > 6 or choice < 1):
                    raise ValueError  #this will send it to the print message and back to the input option
                match choice:
                    case 1:
                        # Buy BTC
                        buyBTC(m_wallet.capital, m_wallet.shares)
                        tradeAgain()
                        
                    case 2:
                        # Sell BTC
                        sellBTC(m_wallet.capital, m_wallet.shares)
                        tradeAgain()
                        
                    case 3:
                        # See Balance
                        m_wallet.seeBalance(m_wallet.capital, m_wallet.shares)
                        tradeAgain()
                        
                    case 4:
                        print("1 BTC token: $" + str(m_wallet.btc.getPrice()))
                        tradeAgain()
                        
                    case 5:
                        # SEE Buy/Sell History
                        m_ledger.viewTransactions()
                        tradeAgain()
                        
                    case 6:
                        # Exit
                        print("Exiting ...")
                        return
                break
            except ValueError: 
                print("Ivalid input! Try again...")
        
    def exit(self):
        print()
        print("SUMMARY")
        
    menu()

if __name__ == "__main__":
    main()

# NOTES! 
#  Guards to add! 
#     - edge case to catch negative funds
#     - invalid input on bitcoin amount 

