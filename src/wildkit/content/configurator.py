from typing import Any, Optional

from dataclasses import dataclass

from .client import Client


@dataclass
class Gender:
    name: str


@dataclass
class Country:
    name: str
    fullName: str


@dataclass
class Season:
    name: str


@dataclass
class TNVED:
    subjectName: str
    tnvedName: str
    description: str
    isKiz: bool


def get_all_genders(clt: Client) -> list[Gender]:
    j = clt.get("/content/v1/directory/kinds")

    return [Gender(name=x) for x in j.get("data", [])]


def get_all_countries(clt: Client) -> list[Country]:
    j = clt.get("/content/v1/directory/countries")

    return [Country(**x) for x in j.get("data", [])]


def get_all_seasons(clt: Client) -> list[Season]:
    j = clt.get("/content/v1/directory/seasons")

    return [Season(name=x) for x in j.get("data", [])]


def get_all_tnveds(clt: Client, category_name: str, tnved_like: str = None) -> list[TNVED]:
    query = {
        "objectName": category_name,
        "tnvedsLike": tnved_like,
    }
    query = {k: v for k, v in query.items() if v}

    j = clt.get("/content/v1/directory/tnved", params=query)

    return [TNVED(**x) for x in j.get("data", [])]


@dataclass
class Limits:
    freeLimits: int
    paidLimits: int


def get_limits(clt: Client) -> Limits:
    j = clt.get("/content/v1/cards/limits")

    return Limits(**j["data"])


@dataclass
class CardSize:
    chrtID: int
    techSize: str
    skus: list[str]


@dataclass
class Card:
    sizes: list[CardSize]
    mediaFiles: Any
    colors: Any
    updateAt: str
    vendorCode: str
    brand: str
    object: str
    nmID: int
    imtID: int
    objectID: int
    isProhibited: bool
    tags: Any

    def __init__(self, d: dict):
        for k, v in d.items():
            if k == "sizes":
                self.sizes = [CardSize(**x) for x in v]
            else:
                setattr(self, k, v)


def get_all_cards(clt: Client, filter_text_search: Optional[str] = None, filter_with_photo: Optional[bool] = None) -> list[Card]:
    result: list[Card] = []
    limit: int = 1_000

    body = {
        "sort": {
            "cursor": {
                "limit": limit
            },
            "filter": {
                "withPhoto": -1 if filter_with_photo is None else 1 if filter_with_photo else 0
            }
        }
    }
    if filter_text_search:
        body["sort"]["filter"]["textSearch"] = filter_text_search

    while True:
        j = clt.post("/content/v1/cards/cursor/list", json=body)
        cards = j.get("data", []).get("cards", [])
        result.extend(Card(x) for x in cards)
        if len(cards) < limit:
            break
        with body["sort"]["cursor"] as cur:
            cur["updateAt"] = result[-1].updateAt
            cur["nmID"] = result[-1].nmID

    return result


def get_cards_by_vendor_codes(clt: Client, vendor_codes: list[str], allowed_categories_only: bool = False) -> list[Card]:
    body = {
        "vendorCodes": vendor_codes,
        "allowedCategoriesOnly": allowed_categories_only,
    }

    j = clt.post("/content/v1/cards/filter", json=body)
    return [Card(x) for x in j["data"]]
