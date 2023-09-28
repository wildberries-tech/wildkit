from dataclasses import dataclass
from typing import Any

from .client import Client


@dataclass
class CharacteristicInfo:
    objectName: str
    name: str
    required: bool
    unitName: str
    maxCount: int
    popular: bool
    charcType: int

    def is_numeric(self):
        return self.charcType == 4

    def is_string(self):
        return self.charcType in [0, 1]


def get_all_characteristics(clt: Client, category_name: str = None) -> list[CharacteristicInfo]:
    query = {
        "name": category_name,
    }
    query = {k: v for k, v in query.items() if v}

    j = clt.get("/content/v1/object/characteristics/list/filter", params=query)

    return [CharacteristicInfo(**x) for x in j.get("data", [])]


def new_property(name: str, value: Any) -> dict:
    return {
        name: value,
    }


def new_characteristic_category(value: str) -> dict:
    return {
        "Предмет": value,
    }


def new_characteristic_tnved(value: str) -> dict:
    return {
        "ТНВЭД": value,
    }


def new_characteristic_package_width(width_cm: int) -> dict:
    return {
        "Ширина упаковки": width_cm,
    }


def new_characteristic_package_height(height_cm: int) -> dict:
    return {
        "Высота упаковки": height_cm,
    }


def new_characteristic_package_depth(depth_cm: int) -> dict:
    return {
        "Длина упаковки": depth_cm,
    }


def new_characteristic_brand(brand: str) -> dict:
    return {
        "Бренд": brand,
    }


def new_characteristic_colors(colors: list[str]) -> dict:
    return {
        "Цвет": colors,
    }


def new_characteristic_title(title: str) -> dict:
    return {
        "Наименование": title,
    }
