# Battleship (Terminal) — Final Project

This project is a simplified **Classic Battleship** game playable in the terminal.

Ship configuration (10 ships total):
- 1 ship of size 4
- 2 ships of size 3
- 3 ships of size 2
- 4 ships of size 1

**Rule:** ships must not touch each other (not even diagonally).

## How to run

```bash
python main.py
```

No external libraries are required (only Python standard library).

## Input format (player ships)

The board is 10×10:

- Rows: **A–J**
- Columns: **1–10**

When placing ships:
- Size 1 ship: enter **one coordinate**, e.g. `A5`
- Size >1 ship: enter **two coordinates** (start end), e.g. `A1 A4`
  - Must be strictly horizontal or vertical
  - The number of cells must equal the required size

Example:
- size 4: `B2 B5`
- size 1: `J10`

The program validates:
- correct ship sizes (4, 3, 3, 2, 2, 2, 1, 1, 1, 1)
- inside the board
- ships do not touch (even diagonally)

Valid placement is saved into `data/player_ships.csv`.

## Ship CSV format

Both `data/player_ships.csv` and `data/bot_ships.csv` use the same format:

- `ship_id` — numeric
- `size` — ship size
- `cells` — semicolon-separated coordinates, e.g. `A1;A2;A3`

## Game state tracking (CSV)

`data/game_state.csv` is updated after every turn and stores:
- `turn`
- `player_shot`, `player_result`
- `bot_shot`, `bot_result`
- `player_view` and `bot_view` boards after the move

Boards are stored as 10 rows joined by `/`, each row containing 10 characters:
- `.` unknown
- `o` miss
- `X` hit

## Display rules (including “terrain after sink”)

After each move the game prints 2 boards:
- **Your shots vs bot**
- **Bot shots vs you**

When a ship is fully destroyed:
- every surrounding cell (8 directions) is automatically marked as **miss** (`o`) in that attacker’s view.

## Bot AI (simple + smart)

Bot behavior:
1. **Random mode**: shoots random untested cells.
2. **After first hit**: tries adjacent cells (up/down/left/right).
3. **After second hit**: locks axis (horizontal/vertical) and continues along that axis until the ship is destroyed.
4. When destroyed: returns to random mode.

## Design decisions

- Only standard library is used (csv, random, os).
- CSVs are simple and human-readable.
- The game stores only “views” (what each side knows), as required.

## Folder structure

```
├─ main.py
├─ data/
│  ├─ player_ships.csv
│  ├─ bot_ships.csv
│  ├─ game_state.csv
├─ src/
│  ├─ ship_input.py
│  ├─ bot_generation.py
│  ├─ gameplay.py
│  └─ utils.py
├─ outputs/
└─ requirements.txt
```
