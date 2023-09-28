import dataclasses
from typing import Any

from dataclasses import dataclass

from .client import Client


def generate_barcodes(clt: Client, count: int) -> list[str]:
    body = {
        "count": count,
    }

    j = clt.post("/content/v1/barcodes", json=body)

    return j.get("data", [])


@dataclass
class CreateCardSize:
    techSize: str
    wbSize: str
    price: int
    skus: list[str]


@dataclass
class CreateCard:
    characteristics: list[Any]
    vendorCode: str
    sizes: list[CreateCardSize]


def create_cards(clt: Client, cards: list[CreateCard]) -> list[str]:
    body = [[dataclasses.asdict(c) for c in cards]]

    j = clt.post("/content/v1/cards/upload", json=body)

    return j.get("data", [])


@dataclass
class CardCreateError:
    object: str
    vendorCode: str
    updateAt: str
    objectID: int
    errors: list[str]


def get_errors(clt: Client) -> list[CardCreateError]:
    j = clt.get("/content/v1/cards/error/list")

    return [CardCreateError(**x) for x in j.get("data", [])]


def attach_photo_to_card(clt: Client, card_vendor_code: str, photo_number: int, filename: str):
    headers = {
        "X-Vendor-Code": card_vendor_code,
        "X-Photo-Number": str(photo_number),
    }
    files = {
        "uploadfile": open(filename, "rb")
    }
    _ = clt.post("/content/v1/media/file", headers=headers, files=files)

