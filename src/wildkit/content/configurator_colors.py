from dataclasses import dataclass

from .client import Client


@dataclass
class Color:
    name: str
    parentName: str


def configurator_get_all_colors(clt: Client) -> list[Color]:
    j = clt.get("/content/v1/directory/colors")

    return [Color(**x) for x in j.get("data", [])]
