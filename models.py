from sqlalchemy import Column, String, Integer, Text
from database import Base


class Recipe(Base):
    __tablename__ = "Recipe"
    recipe_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True, nullable=False)
    views = Column(Integer)
    time_to_cook = Column(Integer)
    ingredients = Column(String)
    description = Column(Text)
