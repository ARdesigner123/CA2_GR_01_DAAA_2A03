# Group members info
group_members = [
    "Stephen Bermudo (2442657)",
    "Aaron Ng (2442631)"
]

from trie_editor import TrieEditor, Trie
from feature_wildcard_search import WildcardSearchFeature

# Function to display the banner
def print_banner():
    print("*****************************************************************")
    print("* ST1507 DSAA: Predictive Text Editor (using tries)             *")
    print("*---------------------------------------------------------------*")
    print("*                                                               *")
    print("* - Done by: Stephen Bermudo (2442657) & Aaron Ng (2442631)     *")
    print("* - Class DAAA/2B/10                                            *")
    print("*                                                               *")
    print("*****************************************************************\n\n")

# Function to display the menu
def display_menu():
    print("Please select your choice ('1','2','3','4','5','6','7'):")
    print("    1. Construct/Edit Trie")
    print("    2. Predict/Restore Text")
    print("    ----------------------------------------------------")
    print("    3. Extra Feature One (Stephen Bermudo):")
    print("    4. Extra Feature Two (Stephen Bermudo):")
    print("    ----------------------------------------------------")
    print("    5. Extra Feature One (Aaron Ng):")
    print("    6. Extra Feature Two (Aaron Ng):")
    print("    ----------------------------------------------------")
    print("    7. Exit")
    
# Main program loop
def main():
    print_banner()  # Show banner only once
    trie_editor = TrieEditor()

    while True:
        display_menu()
        choice = input("Enter choice: ").strip()
        
        if choice == '1':
            print("You selected Option 1: Construct/Edit Trie\n")
            trie_editor.command_prompt()
        elif choice == '2':
            print("You selected Option 2: Predict/Restore Text\n")
            # Call your function here
        elif choice == '3':
            print("You selected Extra Feature One (Stephen Bermudo)\n")
            # Call your function here
        elif choice == '4':
            print("You selected Extra Feature Two (Stephen Bermudo)\n")
            # Call your function here
        elif choice == '5':
            print("You selected Extra Feature One (Aaron Ng): Wildcard Search\n")
            feature = WildcardSearchFeature(Trie)  #Pass Trie class
            feature.run()
        elif choice == '6':
            print("You selected Extra Feature Two (Aaron Ng)\n")
            # Call your function here
        elif choice == '7':
            print("Exiting the program. Goodbye!\n")
            break
        else:
            print("Invalid choice! Please enter a number from 1 to 7.\n")

if __name__ == "__main__":
    main()