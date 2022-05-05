from src.client import NetworkCli
import logging

def main():
    #SERVER_IP = "167.172.152.60"
    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 5555
    logging.getLogger().setLevel(logging.INFO)
    cli = NetworkCli(SERVER_IP, SERVER_PORT)
    cli.main()


# Using the special variable
# __name__
if __name__ == "__main__":
    main()