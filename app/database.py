from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pymysql

# # MySQL database configuration
db_config = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': 3306,
    'database': 'mspr-db',
}

# # MySQL connection URL
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:root@db:3306/mspr-db"

# # Create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

