import math
import webbrowser
import signal

from zlibtui.browser import *
from zlibtui.ui import *
from zlibtui.search import *


class App:
    def __init__(self):
        self.searchBox = SearchBox(term.width-6)
        self.resultsBox = Box(math.ceil(2*term.width/3),\
                        term.height-self.searchBox.height-2,\
                        term.width//3,\
                        self.searchBox.height)
        self.infoBox = Box(term.width//3,\
                        term.height-self.searchBox.height-2,\
                        0,\
                        self.searchBox.height)
        
        self.pageBox = Box(term.width-self.searchBox.width,3,self.searchBox.width,0)
        self.mySearch = Search()
        self.results = []

        self.bookSelected = 0
        self.lowRange = 0
        self.highRange = 50

        self.pageStack = []

        self.focus = "searchBox"

    def main(self):
        '''main loop'''
        def onResize(*args):
            self.refresh()

        signal.signal(signal.SIGWINCH, onResize)
        onResize(term)


        running = True
        with term.fullscreen(), term.hidden_cursor(),term.cbreak():
            print(term.move_xy(0,self.infoBox.height+self.searchBox.height) +
                    " esc:quit | l:open link | p:next page | P:previous page")
            self.searchBox.draw() 
            self.resultsBox.draw()
            self.infoBox.draw()
            self.pageBox.draw()
            while running:
                if self.searchBoxFocus() == "quit" or self.resultsBoxFocus() == "quit":
                    break

    def refresh(self):
        '''Refreshes every element of the app'''
        try:
            print(term.home + term.clear)
            prevbookSelected = self.bookSelected
            self.bookSelected = 0
            self.lowRange = 0
            self.highRange = 50
            self.pageStack = []

            self.searchBox.width = term.width-6

            self.resultsBox.width= math.ceil(2*term.width/3)
            self.resultsBox.height=term.height-self.searchBox.height-2
            self.resultsBox.x=term.width//3
            self.resultsBox.y=self.searchBox.height

            self.infoBox.width = term.width // 3
            self.infoBox.height=term.height-self.searchBox.height-2
            self.infoBox.x=0
            self.infoBox.y=self.searchBox.height

            self.pageBox = Box(term.width-self.searchBox.width,3,self.searchBox.width,0)
            
            if self.focus == "searchbox":
                self.searchBox.draw("green")
                self.resultsBox.draw()

            else:
                self.searchBox.draw()
                self.resultsBox.draw("green")

            self.infoBox.draw()
            self.pageBox.draw()

            self.searchBox.write("")
            
            if self.bookSelected == 0:
                self.scroll()
            while self.bookSelected < prevbookSelected:
                if self.bookSelected != len(self.results)-1:
                    self.bookSelected += 1
                if self.bookSelected >= self.highRange and self.highRange !=\
                len(self.results)-1:
                    self.pageStack.append((self.lowRange,self.highRange))
                    self.lowRange = self.highRange
                    self.bookSelected = self.highRange
                self.scroll()
            
            self.pageBox.clear()
            self.pageBox.write("p."+self.mySearch.searchOptions["page"])

            self.infoBox.clear()
            self.infoBox.write(self.infoBox.content)
            
            print(term.move_xy(0,self.infoBox.height+self.searchBox.height) +
                    " esc:quit | l:open link | p:next page | P:previous page")

        #This avoids crashing when resizing too quickly
        except RuntimeError:
           pass 

    # TODO The common controls for all three windows are simply copy-pasted for
    # now. The common options are: quit, switch focus
    def searchBoxFocus(self):
        self.focus = "searchbox"
        while True:
            self.searchBox.draw("green")
            inp = term.inkey()
            if inp.name == "KEY_BACKSPACE":
                self.searchBox.backspace()
            elif inp.name == "KEY_TAB":
                break
            elif inp.name == "KEY_ENTER":
                self.mySearch.reset()
                self.mySearch.input = self.searchBox.content
                self.showResults()
                break
            elif inp.name == "KEY_ESCAPE":
                return "quit"
            else:
                self.searchBox.write(inp)
        self.searchBox.draw("white")

    def resultsBoxFocus(self):
        self.focus = "resultsbox"
        lowRange = 0
        highRange = len(self.results)
        while True:
            self.resultsBox.draw("green")
            inp = term.inkey()
            if inp.name == "KEY_TAB":
                break
            elif inp.name == "KEY_ENTER":
                self.infoBox.clear()
                info = self.results[self.bookSelected].getDetails()
                self.infoBox.content=info
                if self.infoBox.write(info)==None:
                    self.infoBox.write("Couldn't load the info. "+
                                        "The window is too small!")
            elif inp.name == "KEY_ESCAPE":
                return "quit"
            elif inp == "j":
                if self.bookSelected != len(self.results)-1:
                    self.bookSelected += 1
                if self.bookSelected >= self.highRange and self.highRange !=\
                len(self.results)-1:
                    self.pageStack.append((self.lowRange,self.highRange))
                    self.lowRange = self.highRange
                    self.bookSelected = self.highRange
                self.scroll()

            elif inp == "k":
                if self.bookSelected > self.lowRange:
                    self.bookSelected -= 1
                    self.scroll()
                elif self.bookSelected == self.lowRange and self.lowRange !=0:
                    self.lowRange, self.highRange = self.pageStack.pop()
                    self.bookSelected-= 1
                    self.scroll()

            elif inp == "p":
                self.mySearch.nextPage()
                if self.mySearch.input != "":
                    self.showResults()
            elif inp == "P":
                if self.mySearch.previousPage() != 1 and\
                self.mySearch.input != "":
                    self.showResults()
            elif inp == "l":
                webbrowser.get(BROWSER).open_new(self.results[self.bookSelected].link)
        self.resultsBox.draw("white")

    def showResults(self):
        self.pageBox.clear()
        self.pageBox.write("p."+self.mySearch.searchOptions["page"])
        self.bookSelected = 0
        self.pageStack = []
        self.results = self.mySearch.getResults()
        self.resultsBox.clear()
        for i, book in enumerate(self.results):
            if i == 0:
                self.resultsBox.write(str(i+1)+"."+str(book), "magenta")
            elif self.resultsBox.write(str(i+1)+"."+str(book)) == None:
                self.highRange = i
                self.lowRange =0
                break
        
    def scroll(self):
        self.resultsBox.clear()
        for i in range(self.lowRange, len(self.results)):
            if i == self.bookSelected:
                self.resultsBox.write(str(i+1)+"."+str(self.results[i]), "magenta")
            elif self.resultsBox.write(str(i+1)+"."+str(self.results[i])) == None:
                self.highRange=i
                break
            elif i == len(self.results)-1:
                self.highRange=i

    
if __name__ == "__main__":
    myApp = App()
    myApp.main()
    print(term.home + term.clear)


