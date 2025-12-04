from fastapi import FastAPI

app = FastAPI()


# fastzero/app.py
@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}
