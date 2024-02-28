import random
from app.main import db,Transaction
from datetime import datetime, timedelta
def random_date(start, end):
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

def generate_random_transactions(num_transactions):
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 2, 28)

    transactions = []
    for _ in range(num_transactions):
        transactions.append(Transaction(
            amount_btc=round(random.uniform(0.001, 5.0), 8),
            spent=False,
            created_at=random_date(start_date, end_date)
        ))
    return transactions

def insert_transactions_to_db(transactions):
    db.session.add_all(transactions)
    db.session.commit()

if __name__ == '__main__':
    db.create_all()  
    transactions = generate_random_transactions(10)  
    insert_transactions_to_db(transactions)  
    print("Data generation complete!")
