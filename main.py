# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel

# FastAPI
from fastapi import FastAPI, Body

app = FastAPI()

# Models
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
