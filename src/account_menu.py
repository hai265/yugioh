from src.database_functions import login, register


class AccountMenu:

    def start_menu(self) -> bool:
        func = input("Type 1 to log in with an existing account, or type 2 to register.")
        if func == 1:
            return self.login_proxy()
        else:
            return self.register_proxy()

    def login_proxy(self) -> bool:
        """
        A function which facilitates login via the SQL database.
        Returns:  a boolean which determines whether the login was successful
        """
        name = input("Enter your name: ")
        password = input("Enter your password: ")

        return login(name, password)

    def register_proxy(self, name, password) -> bool:
        """
        A function which facilitates login via the SQL database.

        Args:
            name: A username (maximum 30 characters) that the user wants to register with
            password: A password (maximum 12 characters) that the user wants to register with

        Returns: success: a boolean which determines whether registration was successful
        """
        name = input("Enter your name: ")
        password = input("Enter your password: ")

        return register(name, password)
