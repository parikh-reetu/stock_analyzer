import yfinance as yf
import pandas as pd
from textblob import TextBlob

# stock_symbol = input()


# BEGIN - RSI CALCULATION WRITEN BY CHATGPT
def calculate_rsi(data, window):
    price_diff = data.diff()
    gain = price_diff.mask(price_diff < 0, 0)
    loss = -price_diff.mask(price_diff > 0, 0)
    avg_gain = gain.ewm(span=window, adjust=False).mean()
    avg_loss = loss.ewm(span=window, adjust=False).mean()
    relative_strength = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + relative_strength))
    return rsi


def recommend_stock_rsi(stock_symbol):
    # Fetch historical data for the stock
    try:
        stock = yf.Ticker(stock_symbol)

        # Fetch 1 year of data, adjust as needed
        history = stock.history(period='1y')

        # Calculate the Relative Strength Index (RSI)
        close_prices = history['Close']
        # Using a window of 14 days for RSI calculation
        rsi = calculate_rsi(close_prices, window=14)

        # Make a recommendation based on the RSI strategy
        if rsi.iloc[-1] < 30:  # RSI below 30 indicates an oversold condition
            recommendation = 'Buy'
        elif rsi.iloc[-1] > 70:  # RSI above 70 indicates an overbought condition
            recommendation = 'Sell'
        else:
            recommendation = 'Hold'

        return recommendation
    except Exception as e:
        return "Invalid stock symbol"


# Example usage
# recommendation = recommend_stock_rsi(stock_symbol)
# print(f'Recommendation for {stock_symbol}: {recommendation}')

# END - RSI CALCULATION WRITEN BY CHATGPT


def get_top_headlines(stock_symbol, top=5):
    try:
        symbol = yf.Ticker(stock_symbol)
        news = symbol.news
        headlines = []
        for i in range(min(len(news), top)):
            title = news[i]['title'].lower()
            headlines.append(title)
        return headlines
    except Exception as e:
        return "Invalid stock symbol"


def get_avg_sentiment(headlines):
    avg = 0
    for headline in headlines:
        sentiment = TextBlob(headline).sentiment.polarity
        avg += sentiment

    return avg/len(headlines)


def recommend_stock_sentiment(headlines):
    avg_sentiment = get_avg_sentiment(headlines)
    if avg_sentiment > 0.2:
        return "POSITIVE"
    elif avg_sentiment > -0.2:
        return "NEUTRAL"
    else:
        return "NEGATIVE"


# top_headlines = get_top_headlines(stock_symbol)
# sentiment, rating = recommend_stock_sentiment(top_headlines)
# print("Based on recent articles, the sentiment for " +
#       stock_symbol + " is " + str(round(sentiment, 5)) + " which is " + rating)
