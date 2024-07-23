from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
from datetime import datetime
import requests

app = FastAPI()

API_KEY = '205d7e01d7d5666bf92ee0f8522d5516'
SPORT = 'upcoming'
REGIONS = 'au'
MARKETS = 'h2h'
ODDS_FORMAT = 'decimal'
DATE_FORMAT = 'iso'


class Sport(BaseModel):
    key: str
    group: str
    title: str
    description: str
    active: bool
    has_outrights: bool

class Odds(BaseModel):
    name: str
    price: float

class Market(BaseModel):
    key: str
    last_update: datetime
    outcomes: list[Odds]

class Bookie(BaseModel):
    key: str
    title: str
    last_update: datetime
    markets: list[Market]



class Bet(BaseModel):
    id: str
    sport_key: str
    sport_title: str
    commence_time: str
    home_team: str
    away_team: str
    bookmakers: list[Bookie]



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

@app.get("/get-odds-manual")
def get_odds_manual(SPORT : str):
    response = requests.get(f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds/?apiKey={API_KEY}&regions={REGIONS}&markets={MARKETS}')
    if(response.status_code != 200):
        raise HTTPException(status_code=response.status_code, detail=response.text)
    else:
        bets_json = response.json()
        print(bets_json)

        bets = []
        for bet in bets_json:
            try:
                bet = Bet(**bet)
                bets.append(bet)
            except ValidationError as e:
                print("Validation Error:", e)
                print("Item causing error", bet)
    return bets



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