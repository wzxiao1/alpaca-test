from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime
from alpaca_trade_api import REST
from timedelta import Timedelta


API_KEY = "PKBRL1CPD54RFLCTPPD8"
API_SECRET = "gEEoMSF6Ob7lsgv586PWNsZvZTWhy2R1nDn2Y7tx"
BASE_URL = "https://paper-api.alpaca.markets/v2"

ALPACA = {
    "API_KEY": API_KEY,
    "API_SECRET": API_SECRET,
    "PAPER": True
}



class Bot(Strategy):
    # initialize!
    def initialize(self, symbol:str="SPY", cash_at_risk: float=.65):
        self.symbol = symbol
        self.sleeptime = "24H"
        self.last_trade = None
        self.cash_at_risk = cash_at_risk
        self.api = REST(base_url=BASE_URL, key_id = API_KEY, secret_key=API_SECRET)

    # how much of the stock to buy
    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price, 0)
        return cash, last_price, quantity

    # date of news
    def get_dates(self):
        today = self.get_datetime()
        past = today - Timedelta(days=3)
        return today.strftime('%Y-%m-%d'), past.strftime('%Y-%m-%d')

    # news and sentiment of stock
    def get_news(self):
        today, past = self.get_dates()
        news = self.api.get_news(symbol = self.symbol, start= past, end=today)
        news = [ev.__dict__["_raw"]["headline"] for ev in news] 
        return news


    # trading logic
    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing()
        if cash > last_price:
            if self.last_trade == None:
                news = self.get_news()
                print(news)
                order = self.create_order(
                    self.symbol,
                    quantity,
                    "buy",
                    type="bracket",
                    take_profit_price=last_price * 1.55,
                    stop_loss_price= last_price * 0.98
                )
                self.submit_order(order)
                self.last_trade = "buy"


start_date = datetime(2024, 5, 15)
end_date = datetime(2024, 5, 31)


broker = Alpaca(ALPACA)
strat = Bot(name="mlstrat", broker=broker, parameters={"symbol":"SPY", "cash_at_risk":0.65})

# back testing
strat.backtest(
    YahooDataBacktesting,
    start_date,
    end_date,
    parameters={"symbol":"SPY", "cash_at_risk":0.65}
)