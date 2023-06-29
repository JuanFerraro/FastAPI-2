# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field

# FastAPI
from fastapi import FastAPI, Body, Query, Path, status, Form

app = FastAPI()

# Models
class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str
    state: str
    country: str

class Person(BaseModel):
    first_name: str = Field(min_length=2, max_length=30, example="Sebastian")
    last_name: str
    age: int = Field(gt=0, le=100)
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field (default=None)
    password: str = Field(min_length=8)

    class Config:
        schema_extra = {
            "example":{
                'first_name': 'Juan',
                'last_name': 'Barrios',
                'age': 29,
                'hair_color': 'black',
                'is_maddired': False,
                'password': '*********'
            }
        }

class Login(BaseModel):
    username: str = Field(min_length=3, max_length=20, example='Juan1414')
    password: str = Field(min_length=8, max_length=20)

@app.get(path="/", tags=['home'], status_code=status.HTTP_200_OK) # Path operation decorator -> decorador, metodo get, que viene de app, qie es instancia de fastAPI
def home(): #Patch operation function
    return {'Hola': 'Mundo'}

# Request and Response Body
@app.post(path="/person/new",status_code=status.HTTP_201_CREATED ,tags=['person'], response_model=Person, response_model_exclude={"password"})
def create_person(person: Person = Body()):
    return person

# Validaciones: Query Parameters
@app.get(path="/person/detail", status_code=status.HTTP_200_OK,tags=['person'])
def show_person(
        name: Optional[str] = Query(
            None, 
            min_length=2, 
            max_length=30,
            title="Person Name",
            description="This is the person name. It's between 1 and 30 characters",
            example="Juann"
 
            ),
        age: str = Query(
            title="Person Age", 
            description="This is the person age. It's required",
            example="22"
            )
    ):
    return {name: age}

# Validaciones: Path Parameters
@app.get(path="/person/detail/{person_id}", status_code=status.HTTP_200_OK,tags=['person'])
def show_person(
        person_id: int = Path(
            gt=0,
            title="Person Id",
            description="This is the person id. It's required"
            )
    ):
    return {person_id: "It exists"}

# Validaciones: Request Body
@app.put(path="/person/{person_id}", status_code=status.HTTP_200_OK,tags=['person'])
def update_person(
    person_id: int = Path(
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example=123456
    ),
    person: Person = Body(),
    location: Location = Body()
):
    results = person.dict()
    results.update(location.dict())
    return results

# Login
@app.post(path="/login",tags=['person'], response_model=Login, response_model_exclude={'password'}, status_code=status.HTTP_200_OK)
def login(username: str = Form(), password: str = Form()):
    return Login(username=username, password=password)