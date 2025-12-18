from src import utils

SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

def get_player_ships(out_path="data/player_ships.csv"):
    print("=== Player ship setup ===")
    print("Board is 10x10 (rows A-J, cols 1-10).")
    print("Input format:")
    print("  - size 1:  A5")
    print("  - size >1: A1 A4   (start end, must be straight)")
    print("Ships must NOT touch, even diagonally.\n")

    occupied = set()
    forbidden = set()
    ships = []

    for idx, size in enumerate(SHIP_SIZES, start=1):
        while True:
            try:
                if size == 1:
                    prompt = "Ship %d (size 1) coord: " % idx
                else:
                    prompt = "Ship %d (size %d) start end: " % (idx, size)
                line = input(prompt)
                cells = utils.ship_cells_from_input(line, size)

                for rc in cells:
                    if not utils.in_bounds(rc):
                        raise ValueError("Out of bounds")

                cells_set = set(cells)

                if cells_set & forbidden:
                    raise ValueError("Ships cannot touch each other (including diagonally)")

                ships.append({"size": size, "cells": cells})
                occupied |= cells_set
                for rc in cells_set:
                    forbidden.add(rc)
                    for nb in utils.neighbors8(rc):
                        forbidden.add(nb)

                break
            except ValueError as e:
                print("Invalid input:", e)
                print("Try again.\n")

    utils.write_ships_csv(out_path, ships)
    print("\nSaved player ships to:", out_path)
    return out_path
