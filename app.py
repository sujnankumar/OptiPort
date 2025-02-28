from flask import Flask, render_template, request, redirect, url_for
import io
import base64
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from pypfopt import EfficientFrontier, objective_functions
from pypfopt import black_litterman, risk_models
from pypfopt import BlackLittermanModel
from pypfopt import DiscreteAllocation

app = Flask(__name__)

stock_data = {}  
total_portfolio_value=int()
@app.route('/')
def index():
    return render_template('index.html', stock_data=stock_data)

@app.route('/add_stock', methods=['POST'])
def add_stock():
    
    global stock_data
    stock = request.form.get('stock_ticker')
    view = float(request.form.get('view'))
    confidence = float(request.form.get('confidence'))
    if stock not in stock_data:
        stock_data[stock] = {
            'view': view,
            'confidence': confidence/100
        }
    else:
        stock_data[stock]['view'] = view
        stock_data[stock]['confidence'] = confidence/100


    return redirect(url_for('index'))

@app.route('/remove_stock/<stock>', methods=['GET'])
def remove_stock(stock):
    global stock_data
    if stock in stock_data:
        del stock_data[stock]
    return redirect(url_for('index'))

def generate_plot(amount, name):
    plt.title('Stock Allocation')

    sorted_data = sorted(zip(amount, name), key=lambda x: x[0], reverse=True)
    sorted_amount, sorted_name = zip(*sorted_data)

    plt.figure(figsize=(10, 11))

    labels = [f"{sorted_name[i]}" for i in range(len(sorted_name))]

    def func(pct, allvals):
        return f"{pct:.1f}%"

    num_colors = len(sorted_name)
    colors = plt.cm.get_cmap('tab20', num_colors)

    plt.pie(sorted_amount, labels=None, autopct=lambda pct: func(pct, sorted_amount),
            startangle=140, pctdistance=0.85, colors=colors(np.arange(num_colors)))  
    patches, texts, autotexts = plt.pie(sorted_amount, labels=labels, startangle=140, autopct='',
                                        colors=colors(np.arange(num_colors)))  

    legend_labels = [f"{sorted_name[i]}: ₹{sorted_amount[i]:,.2f}" for i in range(len(sorted_name))]

    custom_legend = [plt.Line2D([0], [0], marker='o', color='w', label=label,
                                markerfacecolor=colors(i), markersize=10) for i, label in enumerate(legend_labels)]

    plt.legend(handles=custom_legend, loc='upper center', bbox_to_anchor=(0.5, 0), ncol=2)
    plt.subplots_adjust(top=1.2)

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()

    return img_base64

@app.route('/optimize', methods=['POST'])
def optimize():
    global total_portfolio_value
    all_stocks=[]
    total_portfolio_value = float(request.form.get('total_portfolio_value'))

    plot_image = None
    tickers_raw=list(stock_data.keys())
    tickers=[]
    for ticker in tickers_raw:
        tickers.append(ticker.upper()+".NS")

    ohlc = yf.download(tickers, period="max")
    print(ohlc)
    prices = ohlc["Adj Close"]
    prices.tail()

    market_prices = yf.download("^NSEI", period="max")["Adj Close"]
    market_prices.head()
        
    mcaps = {}
    for t in tickers:
        stock = yf.Ticker(t)
        mcaps[t] = stock.info["marketCap"]

    S = risk_models.CovarianceShrinkage(prices).ledoit_wolf() 

    delta = black_litterman.market_implied_risk_aversion(market_prices)

    market_prior = black_litterman.market_implied_prior_returns(mcaps, delta, S)

    views=[stock_data[item]['view'] for item in tickers_raw] 
    viewdict=dict(zip(tickers, views))


    bl = BlackLittermanModel(S, pi=market_prior, absolute_views=viewdict)
    confidences=[stock_data[item]['confidence'] for item in tickers_raw] 

    bl = BlackLittermanModel(S, pi=market_prior, absolute_views=viewdict, omega="idzorek", view_confidences=confidences)


    np.diag(bl.omega)


    ret_bl = bl.bl_returns()


    S_bl = bl.bl_cov()

    ef = EfficientFrontier(ret_bl, S_bl)
    ef.add_objective(objective_functions.L2_reg)
    ef.max_sharpe()
    weights = ef.clean_weights()
    weight=dict(weights)
    amounts=list(weight.values())
    name=list(weight.keys())
    amount=[a*total_portfolio_value for a in amounts]
    da = DiscreteAllocation(weights, prices.iloc[-1], total_portfolio_value=total_portfolio_value)
    alloc, leftover = da.greedy_portfolio()

    plot_image=generate_plot(amount,[stock for stock in name])    
    all_stocks = [(value1[:-3], value2) for index, (value1, value2) in enumerate(zip(list(alloc.keys()), list(alloc.values())))]
    return render_template('optimize.html', plot_image=plot_image, all_stocks=all_stocks, leftover=leftover,total_portfolio_value=total_portfolio_value)


if __name__ == '__main__':
    app.run(debug=False)
