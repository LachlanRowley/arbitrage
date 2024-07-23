from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
import requests

app = FastAPI()

API_KEY = '205d7e01d7d5666bf92ee0f8522d5516'
SPORT = 'upcoming'
REGIONS = 'au'
#MARKETS = 
ODDS_FORMAT = 'decimal'
DATE_FORMAT = 'iso'


class Sport(BaseModel):
    key: str
    group: str
    title: str
    description: str
    active: bool
    has_outrights: bool

@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/get-sports", response_model=list[Sport])
def get_sports() -> list[Sport]:
    response = requests.get(f'https://api.the-odds-api.com/v4/sports/?apiKey={API_KEY}')
    if(response.status_code != 200):
        raise HTTPException(status_code=response.status_code, detail=response.text)
    else:
        sports_json = response.json()

        print(sports_json)

        sports = []
        for item in sports_json:
            try:
                sport = Sport(**item)
                sports.append(sport)
            except ValidationError as e:
                print("Validation Error:", e)
                print("Item causing error", item)
    return sports


@app.get("/get-odds")
def get_odds():
    response = requests.get(f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds')
    return response





items = []

#/items?var_name = value gives parameter value
@app.post("/items")
def create_item(item:str):
    items.append(item)
    return items


#{x} means take as variable
@app.get("/items/{item_id}")
def get_item(item_id: int) -> str:
    item = items[item_id]
    return item