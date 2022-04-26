import logging

from src.server import initialize_server


def main():
    logging.getLogger().setLevel(logging.INFO)
    initialize_server()


# Using the special variable
# __name__
if __name__ == "__main__":
    main()
