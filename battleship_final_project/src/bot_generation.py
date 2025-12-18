import random
from src import utils

SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

def try_place_ship(size, forbidden):
    if size == 1:
        r = random.randint(0, utils.BOARD_SIZE - 1)
        c = random.randint(0, utils.BOARD_SIZE - 1)
        rc = (r, c)
        if rc in forbidden:
            return None
        return [rc]

    orientation = random.choice(["H", "V"])
    if orientation == "H":
        r = random.randint(0, utils.BOARD_SIZE - 1)
        c0 = random.randint(0, utils.BOARD_SIZE - size)
        cells = [(r, c0 + i) for i in range(size)]
    else:
        c = random.randint(0, utils.BOARD_SIZE - 1)
        r0 = random.randint(0, utils.BOARD_SIZE - size)
        cells = [(r0 + i, c) for i in range(size)]

    for rc in cells:
        if rc in forbidden:
            return None
    return cells

def generate_bot_ships(out_path="data/bot_ships.csv"):
    ships = []
    forbidden = set()

    for size in SHIP_SIZES:
        placed = None
        for _ in range(10000):
            candidate = try_place_ship(size, forbidden)
            if candidate is None:
                continue
            cells_set = set(candidate)

            ships.append({"size": size, "cells": candidate})
            for rc in cells_set:
                forbidden.add(rc)
                for nb in utils.neighbors8(rc):
                    forbidden.add(nb)
            placed = candidate
            break

        if placed is None:
            raise RuntimeError("Failed to generate bot ships (try again)")

    utils.write_ships_csv(out_path, ships)
    print("Saved bot ships to:", out_path)
    return out_path
