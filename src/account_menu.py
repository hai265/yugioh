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
        :return: success: a boolean which determines whether the login was successful
        """
        name = input("Enter your name: ")
        password = input("Enter your password: ")

        return login(name, password)

    def register_proxy(self) -> bool:
        """
        A function which facilitates login via the SQL database.
        :return: success: a boolean which determines whether registration was successful
        """
        name = input("Enter your name: ")
        password = input("Enter your password: ")

        return register(name, password)
