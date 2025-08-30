from typing import List
from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from sqlalchemy.future import select
from sqlalchemy import desc, update
from database import engine, async_session
import models
import schemas


@asynccontextmanager
async def lifespan(api_app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.post(
    "/recipes/", response_model=schemas.RecipeOut, status_code=status.HTTP_201_CREATED
)
async def add_book(book: schemas.BaseRecipe) -> models.Recipe:
    async with async_session() as session:
        try:
            new_recipe = models.Recipe(**book.model_dump())
            session.add(new_recipe)
            await session.commit()
            await session.refresh(new_recipe)
        except Exception as exc:
            session.rollback()
            raise exc
        finally:
            await session.close()

        return new_recipe


@app.get("/recipes/", response_model=List[schemas.BriefRecipeOut])
async def get_recipes() -> List[models.Recipe]:
    async with async_session() as session:
        try:
            recipes = await session.execute(
                select(
                    models.Recipe.title, models.Recipe.views, models.Recipe.time_to_cook
                ).order_by(desc(models.Recipe.views), models.Recipe.time_to_cook)
            )
        except Exception as exc:
            session.rollback()
            raise exc
        finally:
            await session.close()

    return recipes.all()


@app.get("/recipes/{recipe_id}", response_model=schemas.RecipeOut)
async def get_one_recipe(recipe_id: int):
    async with async_session() as session:
        try:
            recipe = await session.execute(
                select(models.Recipe).where(models.Recipe.recipe_id == recipe_id)
            )
            scalar = recipe.scalar()
            scalar.views = scalar.views + 1
        except Exception as exc:
            session.rollback()
            raise exc
        finally:
            await session.close()

    return scalar
    
