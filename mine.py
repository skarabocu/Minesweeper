from tkinter import *
class Mine(Button):

    xpos = 0
    ypos = 0
    def __init__(self,master=None,*args,**kwargs):
        Button.__init__(self,master,*args,**kwargs)
        self.master=master
        self.button = True







