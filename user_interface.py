

class UserInterface():

    # Function to display the banner
    def print_banner(self):
        print("*****************************************************************")
        print("* ST1507 DSAA: Predictive Text Editor (using tries)             *")
        print("*---------------------------------------------------------------*")
        print("*                                                               *")
        print("* - Done by: Stephen Bermudo (2442657) & Aaron Ng (2442631)     *")
        print("* - Class DAAA/2B/10                                            *")
        print("*                                                               *")
        print("*****************************************************************\n\n")

    # Function to display the menu
    def display_menu(self):
        print("Please select your choice ('1','2','3','4','5','6','7'):")
        print("    1. Construct/Edit Trie")
        print("    2. Predict/Restore Text")
        print("    ----------------------------------------------------")
        print("    3. Extra Feature One (Stephen Bermudo):")
        print("    4. Extra Feature Two (Stephen Bermudo):")
        print("    ----------------------------------------------------")
        print("    5. Advanced Trie Tools (Aaron Ng):")
        print("    6. Keyword Analysis Feature (Aaron Ng):")
        print("    ----------------------------------------------------")
        print("    7. Exit")

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
        print("    \\               (exit\")")
        print("------------------------------------------------------------")
        if show_empty_trie:
            print(">#")
            print("[]")

    def predict_restore(self):
        print("------------------------------------------------------------")
        print("Predict/Restore Text Commands:")
        print("    '~','#','$','?','&','@','!','\\'")
        print("------------------------------------------------------------")
        print("    ~               (read keywords from file to make Trie)")
        print("    #               (display Trie)")
        print("    $ra*nb*w        (list all possible matching keywords)")
        print("    ?ra*nb*w        restore a word using best keyword match")
        print("    &               (write Trie to file)")
        print("    @               (read keywords from file to make Trie)")
        print("    !               (print instructions)")
        print("    \\               (exit\")")
        print("------------------------------------------------------------")