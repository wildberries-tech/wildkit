from dataclasses import dataclass

from .client import Client


@dataclass
class Category:
    objectID: int
    parentID: int
    objectName: str
    parentName: str
    isVisible: bool


def configurator_get_all_categories(clt: Client, name: str = None) -> list[Category]:

    # Get root categories
    j = clt.get("/content/v1/object/parent/all")
    result = [Category(objectID=x["id"], parentID=0, objectName=x["name"], parentName="", isVisible=x["isVisible"]) for x in j.get("data", [])]

    # Get non-root categories
    query = {
        "top": 8_000,
        "name": name,
    }
    query = {k: v for k, v in query.items() if v}

    j = clt.get("/content/v1/object/all", params=query)

    result.extend(Category(**x) for x in j.get("data", []))

    return result
