from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///ass.db")
db = declarative_base()


class Some(db):
    __tablename__ = "some"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)


db.metadata.create_all(engine)
print(Some.query.all())
