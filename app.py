from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = 'c0cd7eb15df470abd4eae059'  # Replace with your real API key
BASE_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/'

@app.route('/', methods=['GET', 'POST'])
def index():
    converted_amount = None
    currencies = []
    if request.method == 'POST':
        from_currency = request.form['from_currency']
        to_currency = request.form['to_currency']
        amount = float(request.form['amount'])

        response = requests.get(BASE_URL + from_currency)
        data = response.json()

        if data['result'] == 'success':
            conversion_rate = data['conversion_rates'][to_currency]
            converted_amount = round(amount * conversion_rate, 2)
            currencies = list(data['conversion_rates'].keys())
        else:
            converted_amount = 'Error fetching rates.'

        return render_template(
            'index.html',
            converted_amount=converted_amount,
            currencies=currencies,
            from_currency=from_currency,
            to_currency=to_currency,
            amount=amount
        )

    response = requests.get(BASE_URL + 'USD')
    print(response.json()) 
    data = response.json()
    if data['result'] == 'success':
        currencies = list(data['conversion_rates'].keys())

    return render_template('index.html', currencies=currencies)

if __name__ == '__main__':
    app.run(debug=True)
