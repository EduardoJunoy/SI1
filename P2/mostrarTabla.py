from sqlalchemy import create_engine
from sqlalchemy.sql import text

DATABASE_TYPE = 'postgresql'  
USERNAME = 'alumnodb'
PASSWORD = 'alumnodb'
HOST = 'localhost'
DATABASE_NAME = 'si1'
PORT = '5432'  

engine = create_engine(f'{DATABASE_TYPE}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}')
connection = engine.connect()

year1 = 2021
year2 = 2022

with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM getTopSales(:year1, :year2)"), {'year1': year1, 'year2': year2})
    for row in result:
        print(row)