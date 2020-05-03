from flection_dictionary.DictLib import *

if __name__ == "__main__":
    files = ["files/pospolite (1).txt", "files/adj.txt", "files/WS_tylko_rzecz.txt", "files/adv.txt", "files/im_nom.txt"]
    file_types = [0, 1, 2, 1, 1]
    bt = DictLib(files, file_types)  # creates WordLib structure
    # bt.print_word("amatorsko")
    # biel = bt.find("biały")
    # for b in biel:
    #     print(b)

    # bt.print_word("biały")

    # bt.save()
    # dl = bt.load()
    print("Załadowany")
    while True:
        input_ = input()
        if input_ == "exit":
            break
        lexemes = bt.find(input_)
        if lexemes:
            for b in lexemes:
                print(b)
        # bt.find(input_)
    # bt.delete()
