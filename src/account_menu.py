from src.database_functions import login, register, user_exists


def display_prompt() -> dict:
    """
    Displays the login prompt, asking the user to either log in with an existing account or register.
    :return: a dictionary containing the user stats for either a new or returning user.
             the dict will contain a string for the username and three integers for wins/losses/draws.
    """

    func = input("Type 1 to log in with an existing account, or type 2 to register: ")
    while func != '1' and func != '2':
        print("Invalid option. Please try again.")
        func = input("Type 1 to log in with an existing account, or type 2 to register: ")

    if func == "1":
        return login_proxy()
    else:  # func must be "2", otherwise.
        return register_proxy()


def login_proxy() -> dict:
    """
    A function which facilitates login via the SQL database and gets the user's stats on success.
    :return: result: a dict containing the user's name, total wins, total losses, and total draws.
    """
    name = ""
    password = ""
    existing_user = False
    result = {"name": "", "wins": -1, "losses": -1, "draws": -1}
    while not existing_user:
        while not 0 < len(name) < 21:
            name = input("Enter a valid username (max. 20 characters): ")

        if not 0 < len(name) < 21:
            print("username must be within specified length. Please try again.")
            name = ""
            continue

        existing_user = user_exists(name)
        if not existing_user:
            print("The specified username does not exist. Please try again.")
            name = ""

    while len(result["name"]) == 0:
        while not 0 < len(password) < 13:
            password = input("Enter a valid password (max. 12 characters: ")

        result = login(name, password)

        if len(result["name"]) == 0:
            print("The provided password is incorrect. Please try again.")

    return result


def register_proxy() -> dict:
    """
    A function which facilitates registration via the SQL database and gets the user's stats on success.
    :return: user_stats: a dict containing the user's name, total wins, total losses, and total draws.
    """
    name = ""
    password = ""
    existing_user = True

    # In order to proceed, the name must be within the accepted length and the user with the name must not exist.
    while not 0 < len(name) < 21 and existing_user is True:
        name = input("Enter a valid username (min. 1 characters, max. 20 characters): ")
        if not 0 < len(name) < 21:
            print("username must be within specified length. Please try again.")
            name = ""
            continue

        existing_user = user_exists(name)
        if existing_user:
            print("A user with that name already exists. Please try again.")
            name = ""

    while not 0 < len(password) < 13:
        password = input("Enter a valid password (max. 12 characters: ")

    return register(name, password)
