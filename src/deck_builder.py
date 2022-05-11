import src.card as card
import csv


def display_prompt() -> list:
    """
    Displays the options to load a preset deck or build a custom one
    :return: a list of cards representing the deck. The list will be empty if something goes wrong
    """

    print('Welcome to the deck building! You can do one of two things here: \n[1] Use preset deck\n[2] build custom '
          'deck\n')
    func = input("Type 1 to load a preset deck, or 2 to build a custom deck: ")

    while func != '1' and func != '2':
        print("Invalid option. Please try again.")
        func = input("Type 1 to load a preset deck, or 2 to build a custom deck: ")

    if func == '1':
        return load_preset_deck()
    else:
        return build_deck()


def load_preset_deck() -> list:
    print('There are currently two decks to pick from: \n[1] Yugi\'s deck \n[2] Kiba\'s deck \n')
    func = input("Type 1 to load a Yugi\'s decks, or 2 to load Kiba\'s deck: ")

    while func != '1' and func != '2':
        print("Invalid option. Please try again.")
        func = input("Type 1 to load a Yugi\'s decks, or 2 to load Kiba\'s deck: ")

    if func == 1:
        return card.create_deck_from_preset('sources/preset3')
    else:
        return card.create_deck_from_preset('sources/preset2')


def build_deck() -> list:
    print('Let\'s build a custom deck! The following are the available commands: \n[1] Add Monster Cards\n[2] Add Spell'
          ' Cards\n[3] Display Monster Cards\n[4] Display Spell Cards\n[5] Done')

    card_names = []
    func = input("Please type the number corresponding to what you would like to do: ")
    while func != '5':
        if func != '1' and func != '2' and func != '3' and func != '4':
            print("Invalid option. Please try again.")
            func = input("Please type the number corresponding to what you would like to do: ")
        else:
            if func == '1':
                card_names += add_monster_cards()
            elif func == '2':
                pass
            elif func == '3':
                print_monster_cards()
            elif func == '4':
                pass

            print(
                'Let\'s keep going. The following are the available commands: \n[1] Add Monster Cards\n[2] Add Spell'
                ' Cards\n[3] Display Monster Cards\n[4] Display Spell Cards\n[5] Done')
            func = input("Please type the number corresponding to what you would like to do: ")

    print('Deck successfully created')
    return list(filter(None, card.create_deck_from_array(card_names)))


def add_monster_cards() -> list:
    card_names = []
    print('NOTE: Any invalid card names will be ignored and the card will not be added to the deck.')
    func = input("Please enter the full monster name to add cards to the deck or \'done\' when you would like to "
                 "stop adding card: ")

    while func != 'done':
        card_names.append(func)
        func = input("Please enter the full monster name to add cards to the deck or \'done\' when you would like to "
                     "stop adding card: ")

    return card_names


def print_monster_cards():
    print('')
    with open('sources/cards.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(str(row[0]))

    print('')


#def main():
#    print(display_prompt())


# Using the special variable
# __name__
#if __name__ == "__main__":
#   main()

