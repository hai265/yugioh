import logging

from src.server import YugiohServer


def main():
    server = YugiohServer("0.0.0.0", 5555)
    logging.getLogger().setLevel(logging.INFO)
    server.initialize_server()


# Using the special variable
# __name__
if __name__ == "__main__":
    main()
