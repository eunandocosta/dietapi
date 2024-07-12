from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:chuck@db:3306/dietas"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db(app):
    with app.app_context():
        from models.model import Dieta, Refeicao, Alimento
        Base.metadata.create_all(bind=engine)
