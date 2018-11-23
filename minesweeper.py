from tkinter import *
from tkinter import messagebox
from mine import Mine
from map import Map
from queue import Queue
import leaderboard as lb

class Window(Frame):
    mines = []
    map = Map()
    mineField = map.draw_map()
    openBoxes = 0

    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.init__window()


    def init__window(self):
        lb.create_table()#creates the leaderboard for the first time only
        self.master.title("Minesweeper")
        self.pack(fill = BOTH, expand = 1)
        count=0#counts the mines
        self.scoreBoard = Label(self, text='Your Score: ' + str(self.openBoxes))  # creates the scoreboard
        self.scoreBoard.grid(row = 0, column = int(1), columnspan = 2)  # places the score
        self.highScore = Label(self, text = 'Highest Score: ' + str(lb.get_high_score()))  # displays the highest score
        self.highScore.grid(row = 0, column = int(4), columnspan = 2)  # places the score
        #assigns the bombs to the randomly selected mines and places the mines on the map
        for x in range(1,len(self.mineField)):
            for y in range(len(self.mineField[x])):
                if self.mineField[x][y] == "X":
                    mine = Mine(self, text = "", font = 20,width = 4, command =lambda bomb = True, order = count,
                                    result = str(self.mineField[x][y]): self.find_bomb(bomb,order,result))#create mine
                    mine.xpos = x
                    mine.ypos = y
                    self.mines.append(mine)
                else:
                    mine = Mine(self, text = "", font = 20,width = 4, command = lambda bomb = False, order = count,
                                    result = str(self.mineField[x][y]): self.find_bomb(bomb,order,result))#create mine
                    mine.xpos = x
                    mine.ypos = y
                    self.mines.append(mine)
                self.mines[count].grid(row = x,column = y)
                count = count + 1
        self.board = Button(self, text = "Leader Board", command = self.show_board)
        self.board.grid(row = x + 1,column = 3, columnspan = 2)
    #function for showing the leaderboard from sqlite code
    def show_board(self):
        messagebox.showinfo("Leader Board",lb.show_table())
    #function for finding the bombs
    def find_bomb(self,bomb,order,result):
        currentMine = self.mines[order]#gets the current box
        if currentMine.cget("text") != "FLAG":#if the mine hasn't been flagged
            answer = messagebox.askquestion("Flag?", "Do you want to put a flag?")
            if answer == "yes":
                currentMine.configure(text = "FLAG")#flagges the box
            else:
                answer2 = messagebox.askquestion("Open?","Do you want to open the box?")
                if answer2 == "yes":#opens the box
                    if bomb is True:#checks if there is a bomb
                        currentMine.configure(text = result, state = DISABLED)  # opens the box
                        messagebox.showinfo("Game Over", "You have stepped on a mine!! The Game Is Over!!!\nYour Final Score:"
                                            + str(self.openBoxes))#game ends if a bomb comes out
                        lb.add_player(self.openBoxes)  # adds the score to the leaderboard
                        exit()#exit the game
                    elif bomb is False:#if there is no bomb
                        currentMine.configure(text = result, state = DISABLED)#opens the box
                        self.openBoxes += 1
                        self.cascade(currentMine)#cascade function
                        self.scoreBoard.configure(text = "Score: " + str(self.openBoxes))#establishes the score
        elif currentMine.cget("text") == "FLAG":#if the box have been flagged
            answer3 = messagebox.askquestion("Open?","Do you want to open the box?")
            if answer3 == "yes":#opens the box
                if bomb is True:#checks if there is a bomb
                    currentMine.configure(text = result, state = DISABLED)  # opens the box
                    messagebox.showinfo("Game Over", "You have stepped on a mine!! The Game Is Over!!!\nYour Final Score:"
                                        + str(self.openBoxes))#ends the game if there was a bomb
                    lb.add_player(self.openBoxes)#adds the score to the leaderboard
                    exit()
                elif bomb is False:
                    currentMine.configure(text = result, state = DISABLED)#opens the box
                    self.openBoxes += 1#increases the number of open boxes
                    self.cascade(currentMine)#cascade function
                    self.scoreBoard.configure(text="Score: " + str(self.openBoxes))  # establishes the score
        if self.openBoxes == 38:#checks if all empty boxes are open
            messagebox.showinfo("Congratulations!!! You won!!!")#congratulations message
            exit()#exits the game
    #main alghoritm of the game for opening the near boxes that doesn't contain mines
    def cascade(self, openedMine):
        q = Queue()
        q.put(openedMine)
        while q.qsize() > 0:
            processedMine = q.get()
            if self.mineField[processedMine.xpos][processedMine.ypos] == "0":
                #adds all the neighbours to the queue
                # northwest
                if processedMine.xpos - 1 >= 0 and processedMine.ypos - 1 >= 0:#cheks if the box exists
                    putMine = self.mines[(processedMine.xpos - 1) * 7 + (processedMine.ypos - 1)]#find the box
                    if putMine.cget("state") != DISABLED:#checks if the mine already opened or not
                        q.put(putMine)#put the box into the queue
                        putMine.configure(text = str(self.mineField[putMine.xpos][putMine.ypos]),state = DISABLED)#opens the box
                        self.openBoxes += 1
                # north
                if processedMine.xpos - 1 >= 0:#checks if the box exists
                    putMine = self.mines[(processedMine.xpos - 1) * 7 + (processedMine.ypos)]#finds the box
                    if putMine.cget("state") != DISABLED:#checks if the mine already opened or not
                        q.put(putMine)#put the box into the queue
                        putMine.configure(text = str(self.mineField[putMine.xpos][putMine.ypos]), state = DISABLED)#opens the box
                        self.openBoxes += 1
                # northeast
                if processedMine.xpos - 1 >= 0 and processedMine.ypos+1 <= 6:  # checks if the box exists
                    putMine = self.mines[(processedMine.xpos - 1) * 7 + (processedMine.ypos+1)]  # finds the box
                    if putMine.cget("state") != DISABLED:  # checks if the mine already opened or not
                        q.put(putMine)  # put the box into the queue
                        putMine.configure(text = str(self.mineField[putMine.xpos][putMine.ypos]),state = DISABLED)  # opens the box
                        self.openBoxes += 1
                # west
                if processedMine.ypos-1 >= 0:  # checks if the box exists
                    putMine = self.mines[(processedMine.xpos) * 7 + (processedMine.ypos-1)]  # finds the box
                    if putMine.cget("state") != DISABLED:  # checks if the mine already opened or not
                        q.put(putMine)  # put the box into the queue
                        putMine.configure(text = str(self.mineField[putMine.xpos][putMine.ypos]),state = DISABLED)  # opens the box
                        self.openBoxes += 1
                # east
                if processedMine.ypos + 1 <= 6:  # checks if the box exists
                    putMine = self.mines[(processedMine.xpos) * 7 + (processedMine.ypos + 1)]  # finds the box
                    if putMine.cget("state") != DISABLED:  # checks if the mine already opened or not
                        q.put(putMine)  # put the box into the queue
                        putMine.configure(text = str(self.mineField[putMine.xpos][putMine.ypos]),state = DISABLED)  # opens the box
                        self.openBoxes += 1
                # southwest
                if processedMine.ypos - 1 >= 0 and processedMine.xpos+1 <= 7: # checks if the box exists
                    putMine = self.mines[(processedMine.xpos+1) * 7 + (processedMine.ypos - 1)]  # finds the box
                    if putMine.cget("state") != DISABLED:  # checks if the mine already opened or not
                        q.put(putMine)  # put the box into the queue
                        putMine.configure(text = str(self.mineField[putMine.xpos][putMine.ypos]),state = DISABLED)  # opens the box
                        self.openBoxes += 1
                # south
                if processedMine.xpos + 1 <= 7:  # checks if the box exists
                    putMine = self.mines[(processedMine.xpos+1) * 7 + (processedMine.ypos)]  # finds the box
                    if putMine.cget("state") != DISABLED:  # checks if the mine already opened or not
                        q.put(putMine)  # put the box into the queue
                        putMine.configure(text = str(self.mineField[putMine.xpos][putMine.ypos]),state = DISABLED)  # opens the box
                        self.openBoxes += 1
                # southeast
                if processedMine.ypos + 1 <= 6 and processedMine.xpos+1<=7:  # checks if the box exists
                    putMine = self.mines[(processedMine.xpos+1) * 7 + (processedMine.ypos + 1)]  # finds the box
                    if putMine.cget("state") != DISABLED:  # checks if the mine already opened or not
                        q.put(putMine)  # put the box into the queue
                        putMine.configure(text = str(self.mineField[putMine.xpos][putMine.ypos]),state = DISABLED)  # opens the box
                        self.openBoxes += 1
root = Tk()
root.geometry("450x300")
Window(root)
root.mainloop()



