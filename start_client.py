from src.client import NetworkCli
import logging

def main():
    logging.getLogger().setLevel(logging.INFO)
    cli = NetworkCli()
    cli.start_game()


# Using the special variable
# __name__
if __name__ == "__main__":
    main()
