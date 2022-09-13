import pdb
import random
from tkinter import *
from tkinter.messagebox import *

class MineSweeper:
    class Mine(Button):
        def __init__(self,root, xy, state, **args):
            Button.__init__(self, root, **args)
            self.xy = xy
            self.num = 0
            self.state = state

    def __init__(self):
        self.root = Tk()
        self.root.title('MineSweeper')

        # set the position of the window to the center of the screen
        self.root.resizable(False, False)

        # Create menu for choosing level
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        def setlevel(self, level):
            if level == 1:
                self.width = 9
                self.height = 9
                self.minenum = 10
            elif level == 2:
                self.width = 16
                self.height = 16
                self.minenum = 40
            else:
                self.width = 30
                self.height = 16
                self.minenum = 99  
            self.start()             
        # create the file_menu
        level_menu = Menu(
            menubar,
            tearoff=0
        )
        level_menu.add_command(label='Beginner', command=lambda: setlevel(self, 1))
        level_menu.add_command(label='Intermediate', command=lambda: setlevel(self, 2))
        level_menu.add_command(label='Expert', command=lambda: setlevel(self, 3))
        menubar.add_cascade(label="Level", menu=level_menu)
                                    
        self.root.mainloop()
    

    def start(self):
        self.rest = self.minenum

        # create Label
        self.label = Label(self.root, text="Mine Number:"+str(self.rest))
        self.label.grid(column=0, row=0, columnspan=self.width, sticky=W, padx=5, pady=5)

        # initiate mines
        mines = random.sample(range(0,self.width*self.height), self.minenum)
        self.mine = [(i%self.width, i//self.height)for i in mines]

        # create Button
        self.buttons = {}
        for x in range(self.width):
            for y in range(self.height):
                self.buttons[(x, y)] = self.Mine(self.root, (x, y), 0, font=('song ti', 12, 'bold'), width=2, height=2, bd=1)
                self.buttons[(x, y)].bind('<ButtonRelease-1>',lambda event:self.left(event.widget))
                self.buttons[(x, y)].bind('<ButtonRelease-3>',lambda event:self.right(event.widget))
                self.buttons[(x, y)].grid(column=x+1, row=y+1, sticky=NSEW)

        # compute mine number for each button
        for x, y in self.mine:
            self.buttons[(x, y)].num = -1
            if (x-1, y-1) in self.buttons.keys() and (x-1, y-1) not in self.mine:
                self.buttons[(x-1, y-1)].num += 1
            if (x, y-1) in self.buttons.keys() and (x, y-1) not in self.mine:
                self.buttons[(x, y-1)].num += 1
            if (x+1, y-1) in self.buttons.keys() and (x+1, y-1) not in self.mine:
                self.buttons[(x+1, y-1)].num += 1
            if (x-1, y) in self.buttons.keys() and (x-1, y) not in self.mine:
                self.buttons[(x-1, y)].num += 1
            if (x+1, y) in self.buttons.keys() and (x+1, y) not in self.mine:
                self.buttons[(x+1, y)].num += 1
            if (x-1, y+1) in self.buttons.keys() and (x-1, y+1) not in self.mine:
                self.buttons[(x-1, y+1)].num += 1
            if (x, y+1) in self.buttons.keys() and (x, y+1) not in self.mine:
                self.buttons[(x, y+1)].num += 1
            if (x+1, y+1) in self.buttons.keys() and (x+1, y+1) not in self.mine:
                self.buttons[(x+1, y+1)].num += 1


    def open_rec(self, xy):
        if xy in self.buttons.keys() and xy not in self.mine and self.buttons[xy].state == 0:
            x, y = xy
            self.buttons[(x, y)].state = 1
            if self.buttons[(x, y)].num == 0:
                self.buttons[(x, y)].configure(relief='flat',bg='white')
                self.open_rec((x-1, y))
                self.open_rec((x, y-1))
                self.open_rec((x+1, y))
                self.open_rec((x, y+1))
            else:
                self.buttons[(x, y)].configure(text=self.buttons[(x, y)].num, relief='flat',bg='white')
        else:
            return

    def left(self, button):
        # click a mine
        if button.num == -1:
            button.configure(relief='flat',bg='white')
            for x, y in self.mine:
                self.buttons[(x,y)].configure(text='☼', fg='red')
            # show the button to restart
            self.show_message(False)
        # expand a whole area that don't have mine in it
        else:
            self.open_rec(button.xy)

    def right(self, button):   
        if button.state == 0 and self.rest > 0:
            button.state = 2
            button['text'] = '☢'
            self.rest -= 1
            self.label['text'] = "Mine Number:"+str(self.rest)
        elif button.state == 2:
            button.state = 0
            button['text'] = ''
            self.rest += 1
            self.label['text'] = "Mine Number:"+str(self.rest)

        # if all mines are tagged, then win the game
        if self.rest == 0:
            for i in self.mine:
                if self.buttons[i].state != 2:
                    return
            self.show_message(True)

    def show_message(self, win):
        if win:
            answer = askyesno(title='You win!(click "no" will quit the game)', 
                            message='Are you sure that you want to restart?')
        else:
            answer = askyesno(title='You lose!(click "no" will quit the game)', 
                            message='Are you sure that you want to restart?')
        if answer:
            self.start()
        else:
            self.root.destroy()

if __name__ == '__main__':
    game = MineSweeper()
