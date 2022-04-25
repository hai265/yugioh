from src.database_functions import login, register


class AccountMenu:

    def start_menu(self) -> bool:
        func = input("Type 1 to log in with an existing account, or type 2 to register.")
        if func == 1:
            self.login_proxy()
        else:
            self.register_proxy()

    def login_proxy(self) -> bool:
        """
        A function which facilitates login via the SQL database.
        :param name: The username associated with the user's account (max 30 characters).
        :param password: The password associated with the user's account (max 12 characters).
        :return: success: a boolean which determines whether the login was successful
        """
        name = input("Enter your name: ")
        password = input("Enter your password: ")

        return login(name, password)


    def register_proxy(self, name, password) -> bool:
        """
        A function which facilitates login via the SQL database.
        :param name: A username (maximum 30 characters) that the user wants to register with
        :param password: A password (maximum 12 characters) that the user wants to register with
        :return: success: a boolean which determines whether registration was successful
        """
        name = input("Enter your name: ")
        password = input("Enter your password: ")

        return register(name, password)
