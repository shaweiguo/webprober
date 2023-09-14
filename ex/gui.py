# Import the necessary library
import tkinter as tk
from tkinter import ttk
# The tempText variable will store the contents of the entry widget
global tempText
# The textVar object will associate the entry widget with the input
global textVar
# Define the winText widget
global winText
# ===================================================================
# Declare the methods that will run the application
def showHideLabelEntry(a):
    if (a == 's'):
        winText.grid()
    elif (a == 'h'):
        winText.grid_remove()
def showHideEntryContent(a):
    global tempText
    global textVar
    if (a == 's'):
        if (tempText != ''):
            textVar.set(tempText)
    if (a == 'h'):
        tempText = textVar.get()
        textVar.set('')
def enableLockDisableEntryWidget(a):
    if (a == 'e'):
        winText.config(state = 'normal')
    elif (a == 'l'):
        winText.config(state = 'disabled')
def boldContentsOfEntryWidget(a):
    if (a == 'b'):
        winText.config(font = 'Arial 14 bold')
    elif (a == 'n'):
        winText.config(font = 'Arial 14')
def passwordEntryWidget(a):
    if (a == 'p'):
        winText.config(show = '*')
    elif (a == 'n'):
        winText.config(show = '')
# ===================================================================
# Declare the method that will create the application GUI
def createGUI():
    createLabelEntry()
    showHideButton()
    showHideContent()
    enableDisable()
    boldOnOff()
    passwordOnOff()
# Create a label and an entry widget to prompt for input and
# associate it with a StringVar object
def createLabelEntry():
    global textVar
    global winText
    winLabel = tk.Label(winFrame, text = 'Enter text:', bg = 'yellow',
    font = 'Arial 14 bold', relief = 'ridge', fg = 'red', bd = 8)
    winLabel.grid(column = 0, row = 0)
    # A StringVar object to accept user input from the keyboard
    textVar = tk.StringVar()
    winText = ttk.Entry(winFrame, textvariable = textVar, width = 20)
    winText.grid(column = 1, row = 0)
# Create two button widgets to show/hide the label and entry widgets
def showHideButton():
    winButtonShow = tk.Button(winFrame, font='Arial 14 bold', text = 'Show the\nentry widget', fg='red',\
                              borderwidth=8, height=3, width=20)
    winButtonShow.grid(column = 0, row = 1)
    winButtonShow.bind('<Button-1>',lambda event,
    a = 's': showHideLabelEntry(a))    
    winButtonHide = tk.Button(winFrame, font = 'Arial 14 bold',\
                              text = 'Hide the\nentry widget',\
                              fg = 'red', borderwidth = 8, height = 3, width = 20)
    winButtonHide.grid(column = 1, row = 1)
    winButtonHide.bind('<Button-1>', lambda event, a = 'h': showHideLabelEntry(a))
# Two button widgets to show/hide the contents of the entry widget
def showHideContent():
    winButtonContentShow = tk.Button(winFrame, font = 'Arial 14 bold',\
                                     text = 'Show the contents\nof the entry widget',\
                                     fg = 'blue', borderwidth = 8, height = 3, width = 20)
    winButtonContentShow.grid(column = 0, row = 2)
    winButtonContentShow.bind('<Button-1>', lambda event,\
                                                        a = 's': showHideEntryContent(a))
    winButtonContentHide = tk.Button (winFrame,\
                                      text = 'Hide the contents\nof the entry widget',\
                                      font = 'Arial 14 bold', fg = 'blue', borderwidth = 8,\
                                      height = 3, width = 20)
    winButtonContentHide.grid (column = 1, row = 2)
    winButtonContentHide.bind ('<Button-1>', lambda event,\
                                                         a = 'h': showHideEntryContent(a))
# Button widgets to enable/disable & lock/unlock the entry widget
def enableDisable():
    winButtonEnableEntryWidget = tk.Button(winFrame,\
                                           text = 'Enable the\nentry widget', font = 'Arial 14 bold',\
                                           fg = 'green', borderwidth = 8, height = 3, width = 20)
    winButtonEnableEntryWidget.grid(column = 0, row = 3)
    winButtonEnableEntryWidget.bind('<Button-1>', lambda event,\
                                                              a = 'e': enableLockDisableEntryWidget(a))
    winButtonDisableEntryWidget = tk.Button(winFrame,\
                                            text = 'Lock the\nentry widget', font = 'Arial 14 bold',\
                                            fg = 'green', borderwidth = 8, height = 3, width = 20)
    winButtonDisableEntryWidget.grid(column = 1, row = 3)
    winButtonDisableEntryWidget.bind('<Button-1>', lambda event,\
                                                               a = 'l': enableLockDisableEntryWidget(a))
# Create two button widgets to switch the "bold" property
# of the entry widget content on or off
def boldOnOff():
    winButtonBoldEntryWidget = tk.Button (winFrame,\
                                          text = 'Bold contents of\nthe entry widget',\
                                          font = 'Arial 14 bold',\
                                          fg = 'brown', borderwidth = 8, height = 3, width = 20)
    winButtonBoldEntryWidget.grid (column = 0, row = 4)
    winButtonBoldEntryWidget.bind ('<Button-1>', lambda event,\
                                                             a = 'b': boldContentsOfEntryWidget(a))
    winButtonNoBoldEntryWidget = tk.Button (winFrame,\
                                            text = 'No bold contents of \nthe entry widget',\
                                            font = 'Arial 14 bold', fg = 'brown', borderwidth = 8,\
                                            height = 3, width = 20)
    winButtonNoBoldEntryWidget.grid (column = 1, row = 4)
    winButtonNoBoldEntryWidget.bind ('<Button-1>', lambda event,\
                                                               a = 'n': boldContentsOfEntryWidget(a))
# Button widgets to convert the entry widget text to a password
def passwordOnOff():
    winButtonPasswordEntryWidget = tk.Button(winFrame,\
                                             text ='Show entry widget \ncontent as password', borderwidth=8,
    font = 'Arial 14 bold', fg = 'grey', height = 3, width = 20)
    winButtonPasswordEntryWidget.grid(column = 0, row = 5)
    winButtonPasswordEntryWidget.bind('<Button-1>', lambda event,\
                                                                a = 'p': passwordEntryWidget(a))
    winButtonNormalEntryWidget = tk.Button(winFrame,\
                                           font = 'Arial 14 bold',\
                                           text = 'Show entry widget \ncontent as normal text',\
                                           fg = 'grey', borderwidth = 8, height = 3, width = 20)
    winButtonNormalEntryWidget.grid(column = 1, row = 5)
    winButtonNormalEntryWidget.bind('<Button-1>', lambda event,\
                                                              a = 'n': passwordEntryWidget(a))
# ===================================================================
# Create the frame using the tk object and run the application
winFrame = tk.Tk()
winFrame.title("Wrap up the basic widgets")
createGUI()
winFrame.mainloop()