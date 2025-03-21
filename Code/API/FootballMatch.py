from datetime import datetime
from typing import TypedDict


class Periods(TypedDict):
    first: int
    second: int


class Venue(TypedDict):
    id: int
    name: str
    city: str


class Status(TypedDict):
    long: str
    short: str
    elapsed: int
    extra: int


class Team(TypedDict):
    id: int
    name: str
    logo: str
    winner: int


class Parameters(TypedDict):
    h2h: str


class Scores(TypedDict):
    home: int
    away: int


class Paging(TypedDict):
    current: int
    total: int


class Fixture(TypedDict):
    id: int
    referee: str
    timezone: str
    date: datetime
    timestamp: int
    periods: Periods
    venue: Venue
    status: Status


class League(TypedDict):
    id: int
    name: str
    country: str
    logo: str
    flag: str
    season: int
    round: str
    standings: bool


class Teams(TypedDict):
    home: Team
    away: Team


class Goals(TypedDict):
    home: int
    away: int


class Score(TypedDict):
    halftime: Scores
    fulltime: Scores
    extratime: Scores
    penalty: Scores


class FootballMatch(TypedDict):
    fixture: Fixture
    league: League
    teams: list[Teams]
    goals: Goals
    score: list[Score]


class FootballMatchesResponse(TypedDict):
    get: str
    parameters: Parameters
    errors: list
    results: int
    paging: Paging
    response: list[FootballMatch]
