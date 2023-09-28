import argparse
import sys
import time
from datetime import datetime

from .tree import print_list_as_tree

import src.wildkit.content as content


def print_list(title: str, elems: list):
    print(f"\n\n{title}:")
    print("\n".join("  " + str(x) for x in elems))


def create_card(clt: content.Client, category: str, vendor_code: str, media_file: str, barcode: str = "", max_wait_time_sec: float = 60.0):
    # if not barcode provided, generate new
    if not barcode:
        barcode = content.generate_barcodes(clt, 1)[0]

    # check our limits
    limits = content.get_limits(clt)
    print(f"Limits: {limits}")

    characteristics = [
        content.new_characteristic_category(category),  # obligatory characteristic - category (aka subject) for new goods
        content.new_characteristic_tnved("6104410000"),
        content.new_characteristic_title("Платье мечты"),
        content.new_characteristic_package_width(30),
        content.new_characteristic_package_height(30),
        content.new_characteristic_package_depth(30),
        content.new_characteristic_brand("MySuperBrand"),
        content.new_characteristic_colors(["красный"])
    ]
    size = content.CreateCardSize(
        techSize="M",   # Whatever format seller prefers to describe size
        wbSize="43",    # Russian-style format of size
        price=100,      # Price in seller's currency
        skus=[barcode]
    )
    card = content.CreateCard(characteristics=characteristics, vendorCode=vendor_code, sizes=[size])
    content.create_cards(clt, [card])

    # Wait for async process to finish
    wait_start = datetime.now()
    created_card: content.Card | None = None
    while (datetime.now() - wait_start).total_seconds() < max_wait_time_sec:
        cards = content.get_all_cards(clt, filter_text_search=vendor_code)
        print(cards)

        created_card = next(iter([c for c in cards if c.vendorCode == vendor_code]), None)
        if created_card:
            break
        # maybe error?
        errors = content.get_errors(clt)
        my_error = next(iter([e for e in errors if e.vendorCode == vendor_code]), None)
        if my_error:
            raise Exception(f"Error creating card {card}: {my_error}")

        time.sleep(1.0)

    if not created_card:
        raise Exception(f"Timeout waiting to create a card {card}")

    content.attach_photo_to_card(clt, vendor_code, 1, media_file)

    print(f"Successfully created: {created_card}")


def print_basic_info(clt: content.Client, selected_category_name_ru: str):
    # categories = content.configurator_get_all_categories(clt)
    # it takes some time to print them all
    # print_list_as_tree("Categories:", categories, "objectID", "parentID")

    characteristics = content.get_all_characteristics(clt, selected_category_name_ru)
    print_list(f"Characteristics for category {selected_category_name_ru}", characteristics)

    colors = content.configurator_get_all_colors(clt)
    print_list_as_tree("Colors:", colors, "name", "parentName")

    genders = content.get_all_genders(clt)
    print_list("Genders", genders)

    countries = content.get_all_countries(clt)
    print_list("Countries", countries)

    seasons = content.get_all_seasons(clt)
    print_list("Seasons", seasons)

    tnveds = content.get_all_tnveds(clt, selected_category_name_ru)
    print_list(f"TNVEDs for category {selected_category_name_ru}", tnveds)


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-t', '--token', help='API token')
    env = arg_parser.parse_args()

    if not env.token:
        raise Exception("Token is missing. Use -t key to pass a token. See https://openapi.wb.ru/en/#section/Description/Authorization how to issue a token.")

    clt = content.Client(env.token)  # restapi client for calling Content methods

    category = "Платья"
    print_basic_info(clt, category)
    create_card(clt, category, f"trendyol-{datetime.now()}", "c:\\p\\superman.jpg")


if __name__ == '__main__':
    sys.exit(main())
