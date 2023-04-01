from flask import Flask
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

# engine = create_engine('sqlite://', connect_args={'check_same_thread':False}, poolclass=StaticPool)
engine = create_engine('sqlite:///db.drones.sqlite3', poolclass=StaticPool)
Session = sessionmaker(bind=engine)

session = Session()
