import os


#Class Created By Stephen
class UserInterface():

    # Function to display the banner (Aaron)
    def print_banner(self):
        print("*****************************************************************")
        print("* ST1507 DSAA: Predictive Text Editor (using tries)             *")
        print("*---------------------------------------------------------------*")
        print("*                                                               *")
        print("* - Done by: Stephen Bermudo (2442657) & Aaron Ng (2442631)     *")
        print("* - Class DAAA/2B/10                                            *")
        print("*                                                               *")
        print("*****************************************************************\n\n")

    # Function to display the menu (Aaron)
    def display_menu(self):
        print("Please select your choice ('1','2','3','4','5','6','7'):")
        print("    1. Construct/Edit Trie")
        print("    2. Predict/Restore Text")
        print("    ----------------------------------------------------")
        print("    3. Visualise Trie Charts (Stephen Bermudo):")
        print("    4. AutoComplete (Stephen Bermudo):")
        print("    ----------------------------------------------------")
        print("    5. Advanced Trie Tools (Aaron Ng):")
        print("    6. Keyword Analysis Feature (Aaron Ng):")
        print("    ----------------------------------------------------")
        print("    7. Exit")
    
    # Function to Display Feature 1 (Aaron)
    def construct_edit(self, show_empty_trie=True):
        print("------------------------------------------------------------")
        print("Construct/Edit Trie Commands:")
        print("    '+','.','?','#','@','~','=','!','\\'")
        print("------------------------------------------------------------")
        print("    +sunshine       (add a keyword)")
        print("    -moonlight      (delete a keyword)")
        print("    ?rainbow        (find a keyword)")
        print("    #               (display Trie)")
        print("    @               (write Trie to file)")
        print("    ~               (read keywords from file to make Trie)")
        print("    =               (write keywords from Trie to file)")
        print("    !               (print instructions)")
        print("    \\              (exit\")")
        print("------------------------------------------------------------")
        # If Trie is empty
        if show_empty_trie:
            print(">#")
            print("[]")
    
    # Function to Display Feature 2 (Stephen)
    def predict_restore(self):
        print("------------------------------------------------------------")
        print("Predict/Restore Text Commands:")
        print("    '~','#','$','?','&','@','!','\\'")
        print("------------------------------------------------------------")
        print("    ~               (read keywords from file to make Trie)")
        print("    #               (display Trie)")
        print("    $ra*nb*w        (list all possible matching keywords)")
        print("    ?ra*nb*w        (restore a word using best keyword match)")
        print("    &               (restore a text using all matching keywords)")
        print("    @               (restore a text using best keywords)")
        print("    !               (print instructions)")
        print("    \\              (exit\")")
        print("------------------------------------------------------------")
        
    def getTrieChart(self):
        print("------------------------------------------------------------")
        print("Trie Chart Drawing Menu:")
        print("    '~','^','!','%','\\'")
        print("------------------------------------------------------------")
        print("    ~               (read keywords from file to make Trie)")
        print("    *               (Visualize Trie Structure with NetworkX)")
        print("    ^               (Visualize Longest Trie Structure with NetworkX)")
        print("    !               (Visualize Specifc Word/Prefix Path with NetworkX)")
        print("    %               (Generate Chart by frequency)")
        print("    \\              (exit\")")
        print("------------------------------------------------------------")

    def autoCompleteGame(self):
        print("------------------------------------------------------------")
        print("Auto Complete Game Menu:")
        print("    '~','#','1','2','\\'")
        print("------------------------------------------------------------")
        print("    ~               (read keywords from file to make Trie)")
        print("    #               (display Trie)")
        print("    1               (Start Round)")
        print("    2               (Review Recent Rounds)")
        print("    \\              (exit\")")
        print("------------------------------------------------------------")

    def Game_UI(self, guesses):
        print("------------------------------------------------------------")
        print("My guesses: ")
        print("------------------------------------------------------------")
        for i, guess in enumerate(guesses, 1):
            if isinstance(guess, tuple):
                word, freq = guess
                print(f"{i} : {word} (freq: {freq})")
            else:
                print(f"{i} : {guess}")
        print("------------------------------------------------------------")




