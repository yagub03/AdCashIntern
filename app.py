from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import uuid
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bitcoin_wallet.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: uuid.uuid4().hex)
    amount_btc = db.Column(db.Float, nullable=False)
    spent = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    return "Welcome to the Bitcoin Wallet API!"

@app.route('/transactions', methods=['GET'])
def list_transactions():
    transactions = Transaction.query.all()
    return jsonify([{'transaction_id': txn.transaction_id, 'amount_btc': txn.amount_btc, 'spent': txn.spent, 'created_at': txn.created_at} for txn in transactions])

@app.route('/balance', methods=['GET'])
def show_balance():
    unspent_txns = Transaction.query.filter_by(spent=False).all()
    total_btc = sum(txn.amount_btc for txn in unspent_txns)
    response = requests.get('http://api-cryptopia.adca.sh/v1/prices/ticker')
    btc_to_eur_rate = next(item for item in response.json()['data'] if item['symbol'] == 'BTC/EUR')['value']
    total_eur = total_btc * float(btc_to_eur_rate)
    return jsonify({'balance_btc': total_btc, 'balance_eur': total_eur})

@app.route('/transfer', methods=['POST'])
def create_transfer():
    amount_eur = request.json['amount_eur']
    response = requests.get('http://api-cryptopia.adca.sh/v1/prices/ticker')
    btc_to_eur_rate = next(item for item in response.json()['data'] if item['symbol'] == 'BTC/EUR')['value']
    amount_btc = amount_eur / float(btc_to_eur_rate)

    if amount_btc < 0.00001:
        return jsonify({'error': 'Transfer amount is too small'}), 400

    unspent_txns = Transaction.query.filter_by(spent=False).order_by(Transaction.created_at).all()

    return jsonify({'message': 'Transfer successful'})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
