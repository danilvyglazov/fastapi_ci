from pydantic import BaseModel, ConfigDict


class BaseRecipe(BaseModel):
    title: str
    views: int = 0
    time_to_cook: int
    ingredients: str
    description: str


class BriefRecipeOut(BaseModel):
    title: str
    views: int
    time_to_cook: int
    model_config = ConfigDict(from_attributes=True)


class RecipeOut(BaseRecipe):
    recipe_id: int
    model_config = ConfigDict(from_attributes=True)
