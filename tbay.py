from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    auction_items = relationship("Item", backref="seller")
    auction_bids = relationship("Bid", backref="buyer")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    seller_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    auction_bids = relationship("Bid", backref="bid_item")
 
class Bid(Base):
    __tablename__ = 'bids'

    id = Column(Integer, primary_key=True)
    bid_amount = Column(Float, nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'))
    buyer_id = Column(Integer, ForeignKey('users.id'))

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
molly = User()
molly.username = "mweasley"
molly.password = "Mollywobbles"
narcissa = User(username="nmalfoy", password="draco")
arthur = User(username='aweasley', password="plugs")
session.add(molly)
session.add(narcissa)
session.add(arthur)
ball = Item(name="Baseball", seller=arthur)
session.add_all([ball])
bid1 = Bid(bid_amount=25.5, bid_item=ball, buyer=molly)
bid2 = Bid(bid_amount=30, bid_item=ball, buyer=narcissa)
session.commit()