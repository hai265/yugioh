import re

from src.database_functions import login, register, user_exists, get_user_stats


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
    result = {"name": "", "wins": -1, "losses": -1, "draws": -1}
    is_valid_username = False
    while not is_valid_username:
        name = input("Enter a valid username (1-20 characters, alphanumeric characters and underscores only.): ")
        is_valid_username = check_username(name)
        existing_user = user_exists(name)
        if not existing_user:
            print("The specified username does not exist. Please try again.")
            is_valid_username = False

    while len(result["name"]) == 0:
        is_valid_password = False
        while not is_valid_password:
            password = input("Enter a valid password (1-12 characters, alphanumeric characters and underscores only): ")
            is_valid_password = check_password(password)
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
    is_valid_username = False
    while not is_valid_username:
        name = input("Enter a valid username (1-20 characters, alphanumeric characters and underscores only): ")
        is_valid_username = check_username(name)
        existing_user = user_exists(name)
        if existing_user:
            print("The specified username already exists. Please try again.")
            is_valid_username = False

    is_valid_password = False
    while not is_valid_password:
        password = input("Enter a valid password (max. 12 characters: ")
        is_valid_password = check_password(password)

    return register(name, password)


def check_username(name: str) -> bool:
    """
    Checks for username validity. A username must be a minimum of 1 character and a maximum of 20 characters in length.
    It must only contain alphanumeric characters and/or underscores.
    Existence of the username is also checked based on which function calls this.
    :param name: The username being checked for validity.
    :return: a boolean indicating whether the username is valid.
    """
    if not 0 < len(name) < 21:
        print("username must be within specified length. Please try again.")
        return False

    is_valid_name = bool(re.match("^[A-Za-z0-9_]+$", name))

    if not is_valid_name:
        print("username must only contain alphanumeric characters or underscores. Please try again.")
        return False

    return True


def check_password(password: str) -> bool:
    """
    Checks for password validity. A password must have a minimum of 1 characters and a maximum of 12 characters.
    It must only contain alphanumeric characters and/or underscores.
    :param password: A string containing the password being checked for validity.
    :return: A boolean indicating whether the password is valid.
    """

    if not 0 < len(password) < 13:
        print("password must be within specified length. Please try again.")
        return False

    is_valid_password = bool(re.match("^[A-Za-z0-9_]+$", password))
    if not is_valid_password:
        print("password must only contain alphanumeric characters or underscores. Please try again.")
        return False

    return True


def user_lookup() -> dict:
    """
    Displays a prompt asking for the name of the user to be looked up.
    The name must be 1-20 characters in length with only alphanumeric characters and/or underscores.
    :return: A dict containing the user's stats.
    """
    is_valid_username = False
    while not is_valid_username:
        name = input("Enter a valid username (1-20 characters, alphanumeric characters and underscores only.): ")
        is_valid_username = check_username(name)
        if is_valid_username:
            result = get_user_stats(name)
            if result["name"] == "":
                print("The username specified does not exist. Please try again.")
                is_valid_username = False
    print(result)
    return result
