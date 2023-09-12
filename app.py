from flask import Flask, render_template, request
from stocks import recommend_stock_rsi, recommend_stock_sentiment, get_top_headlines

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def result():
    user_input = request.form.get('user_input')
    # Process the user input and generate a result
    buy_sell = recommend_stock_rsi(user_input)
    sentiment = recommend_stock_sentiment(user_input)
    headlines = get_top_headlines(user_input)
    return render_template('result.html', buy_sell=buy_sell, sentiment=sentiment, headlines=headlines)


if __name__ == '__main__':
    app.run(port=5000)
