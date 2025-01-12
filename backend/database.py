from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


db_url= "postgresql://postgres:kaddakadda@localhost:5432/SEproject"
engine = create_engine(db_url)
sessionlocal = sessionmaker(autoflush=False , autocommit = False , bind=engine)
Base= declarative_base()



def get_db():
    db = sessionlocal()
    try :
        yield db 
    finally:
        db.close()

