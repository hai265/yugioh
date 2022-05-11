import src.card as card
import csv


def display_prompt(player_name: str) -> list:
    """
    Display's the options for the user to choose a deck
    Args:
        player_name: The name of the player in question

    Returns: A list of card representing a deck

    """
    print('Welcome to the deck building! You can do one of two things here: \n[1] Use preset deck\n[2] Build custom '
          'deck\n[3] Load a previously saved deck')
    func = input("Please the corresponding number to the action you would like to do: ")

    while func != '1' and func != '2' and func != '3':
        print("Invalid option. Please try again.")
        func = input("Please the corresponding number to the action you would like to do:")

    if func == '1':
        return load_preset_deck()
    elif func == '2':
        deck = build_deck()
        func = input("Would you like to save this deck? Type \'yes\' if you do and anything else if you don't: ")
        if func == 'yes':
            print('Saving deck!')
            #save_user_deck(player_name, deck)
        return deck
    else:
        pass


def load_preset_deck() -> list:
    """
    A function to load one of the present decks created by the developers
    Returns: A list of card objects representing a deck
    """
    print('There are currently two decks to pick from: \n[1] Yugi\'s deck \n[2] Kiba\'s deck \n')
    func = input("Type 1 to load a Yugi\'s decks, or 2 to load Kiba\'s deck: ")

    while func != '1' and func != '2':
        print("Invalid option. Please try again.")
        func = input("Type 1 to load a Yugi\'s decks, or 2 to load Kiba\'s deck: ")

    if func == 1:
        return card.create_list_from_preset('sources/preset3')
    else:
        return card.create_list_from_preset('sources/preset2')


def build_deck() -> list:
    """
    A function that allows the user create a deck
    Returns: A list of card represting a deck
    """
    print('Let\'s build a custom deck! The following are the available commands: \n[1] Add Cards\n[2] Display Cards'
          '\n[3] Done')

    card_names = []
    func = input("Please type the number corresponding to what you would like to do: ")
    while func != '3':
        if func != '1' and func != '2':
            print("Invalid option. Please try again.")
            func = input("Please type the number corresponding to what you would like to do: ")
        else:
            if func == '1':
                card_names += add_cards()
            elif func == '2':
                print_cards()

            print(
                'Let\'s keep going. The following are the available commands: \n[1] Add Cards\n[2] Display Cards'
                '\n[3] Done')
            func = input("Please type the number corresponding to what you would like to do: ")

    print('Deck successfully created')
    return card_names


def add_cards() -> list:
    """
    Add cards to a list of card names
    Returns: A list of card names

    """
    card_names = []
    print('NOTE: Any invalid card names will be ignored and the card will not be added to the deck.')
    func = input("Please enter the full monster name to add cards to the deck or \'done\' when you would like to "
                 "stop adding card: ")

    while func != 'done':
        card_names.append(func)
        func = input("Please enter the full monster name to add cards to the deck or \'done\' when you would like to "
                     "stop adding card: ")

    return card_names


def print_cards():
    """
    Prints all the possible cards that the user can use
    Returns: None

    """
    print('')
    with open('sources/cards.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(str(row[0]))

    print('')


def main():
    print(display_prompt("Devak"))


if __name__ == "__main__":
    main()
