from fastapi import FastAPI, APIRouter, Query, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from typing import Annotated, List
from home_budget.repositories.property import PropertyRepository
from home_budget.models.property import PropertyFilter, PropertyDB, Property

app = FastAPI()

FRONTEND_DIR = Path(__file__).parent.joinpath("frontend")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

api_router = APIRouter(prefix="/api")


@api_router.get("/properties")
def get_properties(filter: Annotated[PropertyFilter, Query()]) -> List[PropertyDB]:
    return PropertyRepository.select(filter)


@api_router.post("/properties")
def create_property(property: Property) -> PropertyDB:
    return PropertyRepository.insert(property)


@api_router.delete("/properties/{property_id}")
def delete_property(property_id: int) -> dict:
    deleted = PropertyRepository.delete(property_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Property not found")
    return {"deleted": True}


@app.get("/")
def get_frontend() -> FileResponse:
    return FileResponse(FRONTEND_DIR.joinpath("index.html"))


app.include_router(api_router)
