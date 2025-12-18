import csv
import random
from src import utils

def ship_by_id(ships, ship_id):
    for s in ships:
        if s["id"] == ship_id:
            return s
    return None

def evaluate_shot(ships, rc):
    for s in ships:
        if rc in s["cells"]:
            s["hits"].add(rc)
            sunk = (s["hits"] == s["cells"])
            return ("hit", s["id"], sunk)
    return ("miss", None, False)

def remaining_ships(ships):
    cnt = 0
    for s in ships:
        if s["hits"] != s["cells"]:
            cnt += 1
    return cnt

def player_choose_move(player_view):
    while True:
        try:
            s = input("Your shot (e.g. B7): ").strip()
            rc = utils.parse_coord(s)
            r, c = rc
            if player_view[r][c] != utils.UNKNOWN:
                print("You already shot there. Choose another cell.")
                continue
            return rc
        except ValueError as e:
            print("Invalid coordinate:", e)

def bot_init_state():
    return {
        "mode": "hunt",
        "hits": [],
        "axis": None,     # "H" or "V"
        "tracking_ship": None
    }

def bot_hunt_pick(bot_view):
    choices = []
    for r in range(utils.BOARD_SIZE):
        for c in range(utils.BOARD_SIZE):
            if bot_view[r][c] == utils.UNKNOWN:
                choices.append((r, c))
    return random.choice(choices)

def bot_target_pick(state, bot_view):
    hits = state["hits"]
    axis = state["axis"]

    def is_free(rc):
        r, c = rc
        return bot_view[r][c] == utils.UNKNOWN

    if not hits:
        return bot_hunt_pick(bot_view)

    if axis is None:
        for rc in reversed(hits):
            nbs = utils.neighbors4(rc)
            random.shuffle(nbs)
            for nb in nbs:
                if is_free(nb):
                    return nb
        return bot_hunt_pick(bot_view)

    rows = [rc[0] for rc in hits]
    cols = [rc[1] for rc in hits]

    if axis == "H":
        r = rows[0]
        minc = min(cols)
        maxc = max(cols)
        # try extend right then left (or vice versa)
        candidates = [(r, maxc + 1), (r, minc - 1)]
    else:
        c = cols[0]
        minr = min(rows)
        maxr = max(rows)
        candidates = [(maxr + 1, c), (minr - 1, c)]

    random.shuffle(candidates)
    for rc in candidates:
        if utils.in_bounds(rc) and is_free(rc):
            return rc

    # fallback: try any adjacent to any hit
    for rc in hits:
        for nb in utils.neighbors4(rc):
            if is_free(nb):
                return nb

    return bot_hunt_pick(bot_view)

def bot_choose_move(state, bot_view):
    if state["mode"] == "hunt":
        return bot_hunt_pick(bot_view)
    return bot_target_pick(state, bot_view)

def bot_update_state(state, shot_rc, result, ship_id, sunk):
    if result == "miss":
        return

    # hit
    if state["mode"] == "hunt":
        state["mode"] = "target"
        state["hits"] = [shot_rc]
        state["axis"] = None
        state["tracking_ship"] = ship_id
    else:
        state["hits"].append(shot_rc)
        if state["axis"] is None and len(state["hits"]) >= 2:
            a = state["hits"][0]
            b = state["hits"][1]
            if a[0] == b[0]:
                state["axis"] = "H"
            elif a[1] == b[1]:
                state["axis"] = "V"

    if sunk:
        state["mode"] = "hunt"
        state["hits"] = []
        state["axis"] = None
        state["tracking_ship"] = None

def play(player_ships_path="data/player_ships.csv",
         bot_ships_path="data/bot_ships.csv",
         game_state_path="data/game_state.csv"):

    player_ships = utils.read_ships_csv(player_ships_path)
    bot_ships = utils.read_ships_csv(bot_ships_path)

    own_ship_cells = set()
    for s in player_ships:
        own_ship_cells |= set(s["cells"])


    player_view = utils.create_board(utils.UNKNOWN)
    bot_view = utils.create_board(utils.UNKNOWN)

    bot_state = bot_init_state()

    with open(game_state_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "turn",
            "player_shot", "player_result",
            "bot_shot", "bot_result",
            "player_view", "bot_view"
        ])

    turn = 1
    print("\n=== GAME START ===")
    while True:
        utils.print_two_boards(player_view, bot_view, own_ship_cells)

        # player move
        p_rc = player_choose_move(player_view)
        p_result, p_ship_id, p_sunk = evaluate_shot(bot_ships, p_rc)
        pr, pc = p_rc
        player_view[pr][pc] = utils.HIT if p_result == "hit" else utils.MISS
        if p_sunk:
            s = ship_by_id(bot_ships, p_ship_id)
            utils.mark_surrounding_as_miss(player_view, s["cells"])

        if remaining_ships(bot_ships) == 0:
            utils.print_two_boards(player_view, bot_view, own_ship_cells)
            print("\nYou win! All bot ships destroyed.")
            bot_rc = None
            bot_result = ""
            _append_state(game_state_path, turn, p_rc, p_result, bot_rc, bot_result, player_view, bot_view)
            break

        # bot move
        b_rc = bot_choose_move(bot_state, bot_view)
        b_result, b_ship_id, b_sunk = evaluate_shot(player_ships, b_rc)
        br, bc = b_rc
        bot_view[br][bc] = utils.HIT if b_result == "hit" else utils.MISS
        bot_update_state(bot_state, b_rc, b_result, b_ship_id, b_sunk)
        if b_sunk:
            s = ship_by_id(player_ships, b_ship_id)
            utils.mark_surrounding_as_miss(bot_view, s["cells"])

        _append_state(game_state_path, turn, p_rc, p_result, b_rc, b_result, player_view, bot_view)

        if remaining_ships(player_ships) == 0:
            utils.print_two_boards(player_view, bot_view, own_ship_cells)
            print("\nBot wins! All your ships destroyed.")
            break

        turn += 1

def _append_state(game_state_path, turn, p_rc, p_res, b_rc, b_res, player_view, bot_view):
    with open(game_state_path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            turn,
            utils.coord_str(p_rc) if p_rc else "",
            p_res,
            utils.coord_str(b_rc) if b_rc else "",
            b_res,
            utils.board_to_view_string(player_view),
            utils.board_to_view_string(bot_view)
        ])
