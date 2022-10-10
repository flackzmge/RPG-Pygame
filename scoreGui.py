from tkinter import *
import sqlite3
import tkinter.ttk as ttk

def addScoreGui(score):
    scoreGui = Tk()
    scoreGui.title('Enter Highscore')
    scoreGui.geometry("200x200")
    SearchFrame = Frame(scoreGui)
    SearchFrame.place(x=25,y=50)
    SearchVar = StringVar()
    SearchLabel = Label(SearchFrame,text="Name")
    SearchBox = Entry(SearchFrame,textvariable=SearchVar, width=22,bd=5,state=DISABLED)
    SearchButton = Button(SearchFrame,text="Enter",state=DISABLED,command=lambda : addScoreToDB(SearchBox,score,scoreGui))
    SearchLabel.pack(side=TOP)
    SearchBox.pack(side=TOP)
    SearchButton.pack(side=TOP)

    SearchButton.config(state='normal')
    SearchBox.config(state='normal')
    scoreGui.resizable(0,0)
    scoreGui.mainloop()



def addScoreToDB(SearchBox,score,scoreGui):
    choice=SearchBox.get()
    print(choice)
    connection = sqlite3.connect("highscore.db")
    cursor = connection.cursor()
    values = tuple((str(choice),int(score)))
    cursor.execute('''
    INSERT INTO {}
    VALUES {}
    '''.format('highscorers',values))
    connection.commit()
    scoreGui.destroy()
    displayScores()

def displayScores():
    connection = sqlite3.connect("highscore.db")
    cursor = connection.cursor()
    cursor.execute('''
    SELECT * FROM {}
    ORDER BY Score DESC;
    '''.format('highscorers'))
    data = cursor.fetchall()
    print(data)
    tableGui = Tk()
    tableGui.title('HighScores')
    tableGui.geometry("200x300")
    TableFrame = Frame(tableGui)
    TableFrame.place(x=25,y=50)
    
    tableScroll = Scrollbar(TableFrame)
    table = ttk.Treeview(TableFrame,yscrollcommand=tableScroll.set)
    table.pack()
    tableScroll.config(command=table.yview)

    table['columns'] = ('Name','Score')

    table.column('#0',stretch=NO,width=0)
    table.column('Name',anchor=CENTER,width=80)
    table.column('Score',anchor=CENTER,width=80)

    table.heading('#0',text='',anchor=CENTER)
    table.heading('Name',text='Name',anchor=CENTER)
    table.heading('Score',text='Score',anchor=CENTER)

    for scores in data:
        table.insert(parent='',index='end',text='',values=scores)

