from sqlalchemy import create_engine
from models import Base

engine = create_engine("sqlite:///dse_compass.db")

Base.metadata.create_all(engine)

print("Database created successfully!")