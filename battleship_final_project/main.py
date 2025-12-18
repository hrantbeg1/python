from src import utils
from src import ship_input
from src import bot_generation
from src import gameplay

def main():
    utils.ensure_dirs()
    ship_input.get_player_ships("data/player_ships.csv")
    bot_generation.generate_bot_ships("data/bot_ships.csv")
    gameplay.play("data/player_ships.csv", "data/bot_ships.csv", "data/game_state.csv")

if __name__ == "__main__":
    main()
