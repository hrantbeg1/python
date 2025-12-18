import csv
import os

BOARD_SIZE = 10
LETTERS = "ABCDEFGHIJ"
UNKNOWN = "."
MISS = "o"
HIT = "X"
SHIP = "&"

def ensure_dirs():
    os.makedirs("data", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)
    os.makedirs("src", exist_ok=True)

def parse_coord(s):
    s = s.strip().upper()
    if len(s) < 2:
        raise ValueError("Coordinate too short")
    row_char = s[0]
    if row_char not in LETTERS:
        raise ValueError("Row must be A-J")
    num = s[1:]
    if not num.isdigit():
        raise ValueError("Column must be 1-10")
    col = int(num)
    if col < 1 or col > BOARD_SIZE:
        raise ValueError("Column must be 1-10")
    r = LETTERS.index(row_char)
    c = col - 1
    return (r, c)

def coord_str(rc):
    r, c = rc
    return LETTERS[r] + str(c + 1)

def in_bounds(rc):
    r, c = rc
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE

def neighbors8(rc):
    r, c = rc
    out = []
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                out.append((nr, nc))
    return out

def neighbors4(rc):
    r, c = rc
    out = []
    for dr, dc in ((-1,0), (1,0), (0,-1), (0,1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
            out.append((nr, nc))
    return out

def cells_from_two_coords(a, b):
    ra, ca = a
    rb, cb = b
    if ra == rb:
        step = 1 if cb >= ca else -1
        return [(ra, c) for c in range(ca, cb + step, step)]
    if ca == cb:
        step = 1 if rb >= ra else -1
        return [(r, ca) for r in range(ra, rb + step, step)]
    raise ValueError("Ship must be horizontal or vertical")

def ship_cells_from_input(line, expected_size):
    line = line.strip().replace(",", " ").replace(";", " ").replace("-", " ")
    parts = [p for p in line.split() if p]
    if expected_size == 1:
        if len(parts) != 1:
            raise ValueError("For size 1, enter exactly one coordinate, e.g. A5")
        return [parse_coord(parts[0])]
    if len(parts) != 2:
        raise ValueError("For size >1, enter two coords: start end, e.g. A1 A4")
    a = parse_coord(parts[0])
    b = parse_coord(parts[1])
    cells = cells_from_two_coords(a, b)
    if len(cells) != expected_size:
        raise ValueError("Expected size %d, but got %d cells" % (expected_size, len(cells)))
    return cells

def create_board(fill=UNKNOWN):
    return [[fill for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def board_to_view_string(board):
    return "/".join("".join(row) for row in board)

def write_ships_csv(path, ships):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ship_id", "size", "cells"])
        for i, ship in enumerate(ships, start=1):
            cells = ";".join(coord_str(rc) for rc in ship["cells"])
            w.writerow([i, ship["size"], cells])

def read_ships_csv(path):
    ships = []
    with open(path, "r", newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            size = int(row["size"])
            cells = [parse_coord(x) for x in row["cells"].split(";") if x.strip()]
            ships.append({"id": int(row["ship_id"]), "size": size, "cells": set(cells), "hits": set()})
    return ships

def mark_surrounding_as_miss(target_board, ship_cells):
    marked = []
    ship_cells = set(ship_cells)
    for rc in ship_cells:
        for nb in neighbors8(rc):
            if nb in ship_cells:
                continue
            r, c = nb
            if target_board[r][c] == UNKNOWN:
                target_board[r][c] = MISS
                marked.append(nb)
    return marked

def print_two_boards(player_view, bot_view, own_ship_cells=None):
    header_nums = " ".join([str(i).rjust(2) for i in range(1, BOARD_SIZE + 1)])
    print("\nYour shots (vs bot)".ljust(28) + "Bot shots (vs you)")
    print("   " + header_nums + "     " + "   " + header_nums)
    for r in range(BOARD_SIZE):
        left = " ".join(player_view[r][c].rjust(2) for c in range(BOARD_SIZE))

        right_cells = []
        for c in range(BOARD_SIZE):
            ch = bot_view[r][c]
            if own_ship_cells is not None and ch == UNKNOWN and (r, c) in own_ship_cells:
                ch = SHIP
            right_cells.append(ch.rjust(2))
        right = " ".join(right_cells)

        print(LETTERS[r] + "  " + left + "     " + LETTERS[r] + "  " + right)

def all_cells_unknown(board):
    for row in board:
        for v in row:
            if v != UNKNOWN:
                return False
    return True
