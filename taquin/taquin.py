# -*- coding: utf-8 -*-
 
import tkinter as tk
import tkinter.font as tkFont
from random import randint
import time
 
gris = "grey"
noir = "black"
blanc = "white"
 

class Taquin:

    def __init__(self, size):
        self.size = size
        self.makeBoard()


    def makeBoard(self):
        size = self.size
        self.path = []
        self.board = [ 0 ] * (size * size)
        self.refboard = [ 0 ] * (size * size)
        for i in range((size*size)-1):
            self.board[i] = i+1
            self.refboard[i] = i+1
        self.board[(size*size) - 1] = 0
        self.refboard[(size*size) - 1] = 0


    def getXY(self, x, y):
        i = x + y * self.size
        return self.board[i]


    def isOk(self, x, y):
        i = x + y * self.size
        return self.board[i] == self.refboard[i]


    def getblank(self):
        b = 0
        for i in range(self.size * self.size):
            if self.board[i] == 0:
                b = i
                break
        return b
    
    def isWon(self):
        for i in range((self.size*self.size)-1):
            if self.board[i] != i+1:
                return False
        return self.board[(self.size*self.size)-1] == 0


    def update(self, dir, rec = True):
        b = self.getblank()
     
        if dir == 'U' and b > (self.size-1):
            self.board[b] = self.board[b-self.size]
            self.board[b-self.size] = 0
            if rec:
                self.path.append('U')
            return 1
            
        elif dir == 'D' and b < (self.size * (self.size-1)):
            self.board[b] = self.board[b+self.size]
            self.board[b+self.size] = 0
            if rec:
                self.path.append('D')
            return 1

        elif dir == 'L' and (b % self.size) > 0:
            self.board[b] = self.board[b-1]
            self.board[b-1] = 0
            if rec:
                self.path.append('L')
            return 1

        elif dir == 'R' and (b % self.size) < (self.size-1):
            self.board[b] = self.board[b+1]
            self.board[b+1] = 0
            if rec:
                self.path.append('R')
            return 1

        else:
            return 0


    def randomize(self, seed, level):
        self.makeBoard()
        moves = seed * level
        while moves > 0:
            d = 'UDLR'[randint(0, 3)]
            moves -= self.update(d, rec = True)


    def undo(self):
        if len(self.path) > 0:
            move = self.path.pop()
            if move == 'U':
                move = 'D'
            elif move == 'D':
                move = 'U'
            elif move == 'L':
                move = 'R'
            elif move == 'R':
                move = 'L'
            else:
                move = ' '
        else:
            move = ' '
        return move


    def canonizepath(self):
        newpath = []
        p = ' '
        for m in self.path:
            if p == ' ':
                newpath.append(m)
                p = m
            else:
                if (p,m) in (('U', 'D'), ('D', 'U'), ('L', 'R'), ('R', 'L')):
                    newpath.pop()
                    if len(newpath) > 0:
                        p = newpath[-1]
                    else:
                        p = ' '
                else:
                    newpath.append(m)
                    p = m
        self.path.clear()
        for m in newpath:
            self.path.append(m)


class Fenetre:

    def __init__(self, difficulte = 64, taille = 4):
        self.difficulte = difficulte
        self.taille = taille

        self.root = tk.Tk()
        self.root.geometry('600x600')
        self.root.title('Taquin')

        self.menubar = tk.Menu(self.root)
        gamemenu = tk.Menu(self.menubar, tearoff = 0)
        gamemenu.add_command(label="Nouveau jeu 3x3", command = self.newgame3x3)
        gamemenu.add_command(label="Nouveau jeu 4x4", command = self.newgame4x4)
        gamemenu.add_command(label="Nouveau jeu 5x5", command = self.newgame5x5)
        gamemenu.add_command(label="Nouveau jeu 6x6", command = self.newgame6x6)
        gamemenu.add_command(label="Nouveau jeu 8x8", command = self.newgame8x8)
        gamemenu.add_command(label="Nouveau jeu 10x10", command = self.newgame10x10)
        gamemenu.add_separator()
        gamemenu.add_command(label = "Quitter", command = self.root.quit)
        toolmenu = tk.Menu(self.menubar, tearoff = 0)
        toolmenu.add_command(label="Annuler", command = self.undo)
        toolmenu.add_separator()
        toolmenu.add_command(label = "Résoudre", command = self.startSolver)
        toolmenu.add_command(label = "Arrêter", command = self.stopSolver)
        self.menubar.add_cascade(label = "Jeu", menu = gamemenu)
        self.menubar.add_cascade(label = "Outils", menu = toolmenu)
        self.root.config(menu = self.menubar)

        self.board = tk.Canvas(self.root, bg = 'white', height = 800, width = 800)
        self.board.pack()

        self.tfont = tkFont.Font(family='Helvetica', size=32, weight='bold')
        self.gofont = tkFont.Font(family='Helvetica', size=56, weight='bold')


    def play(self):
        self.newgame(self.taille)
        self.root.mainloop()


    def undo(self, e = None):
        move = self.taquin.undo()
        if move == 'U':
            self.up(None, rec=False)
            return True
        elif move == 'D':
            self.down(None, rec=False)
            return True
        elif move == 'L':
            self.left(None, rec=False)
            return True
        elif move == 'R':
            self.right(None, rec=False)
            return True
        else:
            return False


    def solve(self):
        if self.undo() and not self.stop:
            self.root.after(50, self.solve)


    def startSolver(self):
        self.taquin.canonizepath()
        self.stop = False
        self.solve()


    def stopSolver(self):
        self.stop = True


    def newgame3x3(self):
        self.newgame(3)


    def newgame4x4(self):
        self.newgame(4)


    def newgame5x5(self):
        self.newgame(5)


    def newgame6x6(self):
        self.newgame(6)


    def newgame8x8(self):
        self.newgame(8)


    def newgame10x10(self):
        self.newgame(10)


    def newgame(self, taille):
        self.taille = taille
        self.taquin = Taquin(taille)
        self.taquin.randomize(self.difficulte, self.taille)
        self.drawboard()

        self.root.bind('<Up>', self.up)
        self.root.bind('<Down>', self.down)
        self.root.bind('<Left>', self.left)
        self.root.bind('<Right>', self.right)
        self.root.bind('<Button-1>', self.click)
        self.root.bind('<BackSpace>', self.undo)


    def click(self, e):
        mx = int(e.x / (600/self.taille))
        my = int(e.y / (600/self.taille))
        b = self.taquin.getblank()
        bx = b % self.taille
        by = int(b / self.taille)
        if mx == bx and my == by:
            pass
        else:
            if mx == bx:
                if my == by+1:
                    self.down(e, rec = True)
                elif my == by-1:
                    self.up(e, rec = True)
                else:
                    pass
            elif my == by:
                if mx == bx+1:
                    self.right(e, rec = True)
                elif mx == bx-1:
                    self.left(e, rec = True)
                else:
                    pass


    def up(self, e, rec = True):
        self.taquin.update('U', rec)
        if self.taquin.isWon():
            self.gameover()
        else:
            self.drawboard()


    def down(self, e, rec = True):
        self.taquin.update('D', rec)
        if self.taquin.isWon():
            self.gameover()
        else:
            self.drawboard()


    def left(self, e, rec = True):
        self.taquin.update('L', rec)
        if self.taquin.isWon():
            self.gameover()
        else:
            self.drawboard()


    def right(self, e, rec = True):
        self.taquin.update('R', rec)
        if self.taquin.isWon():
            self.gameover()
        else:
            self.drawboard()


    def gameover(self):
        self.drawboard()
        self.board.create_text(300, 300, text='Gagné !', font=self.gofont, fill='red')

        self.root.unbind('<Up>')
        self.root.unbind('<Down>')
        self.root.unbind('<Left>')
        self.root.unbind('<Right>')
        self.root.unbind('<Button-1>')


    def drawboard(self):
        self.board.create_rectangle(0, 0, 600, 600, fill='white')
        for i in range(self.taille):
            for j in range(self.taille):
                self.drawtile(self.board, i*(600/self.taille), j*(600/self.taille), self.taquin.getXY(i, j), self.taquin.isOk(i, j))


    def drawtile(self, canvas, x, y, v, isOk):

        canvas.create_line(x,y,x+(600/self.taille),y,fill='black')
        canvas.create_line(x+1,y+1,x+(600/self.taille)-1,y+1,fill='grey')
        canvas.create_line(x,y,x,y+(600/self.taille),fill='black')
        canvas.create_line(x+1,y+1,x+1,y+(600/self.taille)-1,fill='black')

        if v > 0:
            if isOk:
                col = 'green'
            else:
                col = 'black'
            canvas.create_text(x+(300/self.taille), y+(300/self.taille), text=str(v), font=self.tfont, fill=col)
        else:
            canvas.create_rectangle(x+2, y+2, x+(600/self.taille)-2, y+(600/self.taille)-2, fill='white')



class Texte:

    def __init__(self, difficulte = 64, taille = 4):
        self.difficulte = difficulte
        self.taille = taille


    def play(self):
        self.newgame()

        while True:
            self.drawboard()

            c = input('A vous de jouer : (N) Nouveau, (Q) Quitter, ou flèche (8,4,6,2)')
            if c in ('q', 'Q'):
                return True
            
            if c in ('n', 'N'):
                self.newgame()
            elif c == '8':
                self.up()
            elif c == '6':
                self.right()
            elif c == '4':
                self.left()
            elif c == '2':
                self.down()


    def newgame(self):

        while True:
            t = input('Taille du jeu (3, 4, 5, 6)')
            if t in '3456':
                self.taille = int(t)
                break

        self.taquin = Taquin(self.taille)
        self.taquin.randomize(self.difficulte, self.taille)


    def up(self):
        self.taquin.update('U')
        if self.taquin.isWon():
            self.gameover()
        else:
            self.drawboard()


    def down(self):
        self.taquin.update('D')
        if self.taquin.isWon():
            self.gameover()
        else:
            self.drawboard()


    def left(self):
        self.taquin.update('L')
        if self.taquin.isWon():
            self.gameover()
        else:
            self.drawboard()


    def right(self):
        self.taquin.update('R')
        if self.taquin.isWon():
            self.gameover()
        else:
            self.drawboard()


    def gameover(self):
        self.drawboard()
        print('Bravo! Vous avez gagné!')


    def drawboard(self):
        print('+----' * self.taille + '+')
        for j in range(self.taille):
            print('|    ' * self.taille + '|')
            for i in range(self.taille):
                self.drawtile(self.taquin.getXY(i, j))
            print('|')
            print('|    ' * self.taille + '|')
            print('+----' * self.taille + '+')


    def drawtile(self, v):
        print('| ', end='')
        if v == 0:
            print('  ', end = '')
        elif v < 10:
            print(' ' + str(v), end='')
        else:
            print(str(v), end='')
        print(' ', end='')



mode = 'F'   # Fenetre Tk
#mode = 'T'   # Texte console

taille = 5
difficulte = 64

if __name__ == "__main__":
    if mode == 'F':
        root = Fenetre(difficulte, taille)
    else:
        root = Texte(difficulte, taille)
    root.play()
    
