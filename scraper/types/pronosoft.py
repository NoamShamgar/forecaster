from dataclasses import dataclass
from enum import Enum
from typing import List


class ResultEnum(Enum):
    ONE = "1"
    TWO = "2"
    NOT = "N"


@dataclass
class PronosoftGame:
    game_index: str
    team1: str
    team2: str
    team1score: str
    team2score: str
    result: ResultEnum
    odds_portal_url:str = ""

@dataclass
class PronosoftEvent:
    cycle: str
    date: str
    form_type:str
    games: List[PronosoftGame]
    
