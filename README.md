# AdCash Intern
Backend Services & API Internship Assignment

## Prequisite: 

Clone the repository by using git clonehttps://github.com/yagub03/AdCashIntern.git command and then cd AdCashIntern

## How to run our project:

First, we need to add `python app/main.py` in the terminal, then we open new terminal and add `python generate_data.py`. 

## How to test endpoints:
After getting data, we can use URL http://127.0.0.1:5000 and also /transaction,/balance and also for transfer request, we can use
```curl -X POST http://127.0.0.1:5000/transfer -H "Content-Type: application/json" -d "{\"amount_eur\": 50}" ```
