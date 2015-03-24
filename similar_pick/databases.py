# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from similar_pick.models import Restaurant


engine = create_engine('sqlite:///data/restaurant.db', echo=True)
metadata = MetaData(bind=engine, reflect=True)

restaurant = metadata.tables['restaurant']

from sqlalchemy.orm import mapper
mapper(Restaurant, restaurant)

Session = sessionmaker(bind=engine)
session = Session()
