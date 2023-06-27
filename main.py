from fastapi import FastAPI


app = FastAPI()

@app.get("/") # Path operation decorator -> decorador, metodo get, que viene de app, qie es instancia de fastAPI
def home():
    return {'Hola': 'Mundo'}


