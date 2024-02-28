from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    transaction_id = Column(String, unique=True)
    amount_btc = Column(Float)
    spent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


engine = create_engine('sqlite:///bitcoin_wallet.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
