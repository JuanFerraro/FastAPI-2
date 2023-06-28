# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel

# FastAPI
from fastapi import FastAPI, Body, Query, Path

app = FastAPI()

# Models

class Location(BaseModel):
    city: str
    state: str
    country: str

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

@app.get("/", tags=['home']) # Path operation decorator -> decorador, metodo get, que viene de app, qie es instancia de fastAPI
def home(): #Patch operation function
    return {'Hola': 'Mundo'}

# Request and Response Body
@app.post("/person/new", tags=['person'])
def create_person(person: Person = Body()):
    return person

# Validaciones: Query Parameters
@app.get("/person/detail", tags=['person'])
def show_person(
        name: Optional[str] = Query(
            None, 
            min_length=2, 
            max_length=30,
            title="Person Name",
            description="This is the person name. It's between 1 and 30 characters"
            ),
        age: str = Query(
            title="Person Age", 
            description="This is the person age. It's required"
            )
    ):
    return {name: age}

# Validaciones: Path Parameters
@app.get("/person/detail/{person_id}", tags=['person'])
def show_person(
        person_id: int = Path(
            gt=0,
            title="Person Id",
            description="This is the person id. It's required"
            )
    ):
    return {person_id: "It exists"}

# Validaciones: Request Body
@app.put("/person/{person_id}", tags=['person'])
def update_person(
    person_id: int = Path(
        title="Person ID",
        description="This is the person ID",
        gt=0
    ),
    person: Person = Body(),
    location: Location = Body()
):
    results = person.dict()
    results.update(location.dict())
    return results