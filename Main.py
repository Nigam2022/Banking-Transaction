from tkinter import *
import pandas as pd
import random as rnd
import csv
import shutil
from tempfile import NamedTemporaryFile
import datetime


# Make GUI Window
gui = Tk()
gui.title('Transaction Window')
gui.geometry('900x650+250+35')

df = pd.DataFrame(
    columns=['Account', 'Deposit', 'Withdraw', 'Old_Password', 'New_Password', 'TimeStamp'])  # Transaction Dataframe

# For Display in Table Form on GUI
class Table:

    def __init__(self, root, lst):

        # code for creating table
        for i in range(len(lst)):
            for j in range(len(lst[0])):
                self.e = Entry(root, width=20, fg='blue',
                               font=('Arial', 16, 'bold'))

                self.e.grid(row=i + 16, column=j)
                self.e.insert(END, lst[i][j])

# Finding count of denomination of 10, 500, 1000
def getDeno(x):
    ret = {1000: 0, 500: 0, 10: 0}
    if x >= 1000:
        ret[1000] = x // 1000
        x %= 1000
    if x >= 500:
        ret[500] = x // 500
        x %= 500
    if x >= 10:
        ret[10] = x // 10
        x %= 10
    return ret


# Find Balance of Particular Account
def getBal(acc) :
    ret = list()
    with open('AccountDetails.csv', 'r') as csvfile :
        reader = csv.DictReader(csvfile)
        for row in reader :
            curr = int(row['AccountNumber'])
            if curr == acc :
                ret.append(int(row['Balance']))


    with open('AtmDetails.csv', 'r') as csvfile :
        reader = csv.DictReader(csvfile)
        for row in reader :
            curr = int(row['Account'])
            if curr == acc :
                ret.append(row)

    return ret

# To Change PIN

def pinChange(ac, old, new):
    global df

    found = False

    with open('AccountDetails.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            acc = int(row['AccountNumber'])
            pw = int(row['Password'])
            if acc == ac and pw == old:
                found = True

    if found == False:
        return False


    tempfile = NamedTemporaryFile(mode='w+', delete=False)
    cols = ['CardNumber', 'AccountNumber', 'Balance', 'AccountType', 'Password']

    with open('AccountDetails.csv', 'r+', encoding='utf-8') as csvfile, tempfile:
        reader = csv.DictReader(csvfile)
        writer = csv.DictWriter(tempfile, fieldnames=cols)
        writer.writeheader()

        for row in reader:
            acc = int(row['AccountNumber'])
            pw = int(row['Password'])
            if acc == ac and pw == old:
                row['Password'] = str(new)
                df = df.append({'Account' : str(acc), 'Old_Password': str(old), 'New_Password': str(new), 'TimeStamp': str(datetime.datetime.now())}, ignore_index=True)
            writer.writerow(row)

    shutil.move(tempfile.name, 'AccountDetails.csv')
    return True


# Validate of Given Input for Fund Transfering

def validInput(card1, ac2, amt, pwd):
    with open('AccountDetails.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        found = False
        if amt <= 0 :
            return False

        for row in reader:

            if int(row['CardNumber']) == card1:

                if amt > int(row['Balance']) or pwd != int(row['Password']):
                    return False

            elif int(row['AccountNumber']) == ac2:
                found = True

        return found

# Main Process of Fund Transfering !

def fundTransfer(card1, acc2, amt, pwd):
    global df

    if validInput(card1, acc2, amt, pwd) == False:
        return False

    deno = getDeno(amt)
    tempfile = NamedTemporaryFile(mode='w+', delete=False)

    cols = ['CardNumber', 'AccountNumber', 'Balance', 'AccountType', 'Password']
    atm_cols = ['Account', '10', '500', '1000']
    trans_cols = ['Account', 'Deposit', 'Withdraw', 'Old_Password', 'New_Password', 'TimeStamp']


    with open('AccountDetails.csv', 'r+', encoding='utf-8') as csvfile, tempfile:
        reader = csv.DictReader(csvfile)
        writer = csv.DictWriter(tempfile, fieldnames=cols)
        writer.writeheader()

        for row in reader:
            if int(row['CardNumber']) == card1:
                acc1 = int(row['AccountNumber'])
                row['Balance'] = str(int(row['Balance']) - amt)
                df = df.append({
                    'Account': str(acc1),
                    'Withdraw': str(amt),
                    'TimeStamp': str(datetime.datetime.now())
                }, ignore_index=True)

            elif int(row['AccountNumber']) == acc2:

                row['Balance'] = str(int(row['Balance']) + amt)
                df = df.append({
                    'Account': str(acc2),
                    'Deposit': str(amt),
                    'TimeStamp': str(datetime.datetime.now())
                }, ignore_index=True)
            writer.writerow(row)

    shutil.move(tempfile.name, 'AccountDetails.csv')

    tempfile = NamedTemporaryFile(mode='w+', delete=False)

    with open('AtmDetails.csv', 'r+', encoding='utf-8') as csvfile, tempfile:
        reader = csv.DictReader(csvfile)
        writer = csv.DictWriter(tempfile, fieldnames=atm_cols)
        writer.writeheader()

        for row in reader:
            ac = int(row['Account'])

            if  ac == acc1:
               # print('In AC1')
                row['10'] = str(int(row['10']) - deno[10])
                row['500'] = str(int(row['500']) - deno[500])
                row['1000'] = str(int(row['1000']) - deno[1000])
            elif ac == acc2:
                #print('In AC2')
                row['10'] = str(int(row['10']) + deno[10])
                row['500'] = str(int(row['500']) + deno[500])
                row['1000'] = str(int(row['1000']) + deno[1000])

            writer.writerow(row)

    shutil.move(tempfile.name, 'AtmDetails.csv')
    return True
    # data = pd.read_csv('Atm1.csv')
    # print(data.head())

# Bank Enquiry : task4 and Util4

def Util4() :
    global gui
    ac = int(e31.get())

    res = getBal(ac)
    verdict = Label(gui, bg='black', fg='yellow', font=5)


    if len(res) == 0:
        verdict["text"] = "*** Invalid Input ***"
        verdict.grid(row=23, column=1)
        return

    dataDict = res[1]
    col1 = Label(gui, text = 'Balance', fg = 'red', bg = 'Orange')
    col2 = Label(gui, text = '10_Denomination', fg = 'red', bg = 'Orange')
    col3 = Label(gui, text = '500_Denomination', fg = 'red', bg = 'Orange')
    col4 = Label(gui, text = '1000_Denomination', fg = 'red', bg = 'Orange')

    val1 = Label(gui, text = str(res[0]), fg = 'black', bg = 'Green')
    val2 = Label(gui, text = dataDict['10'], fg = 'black', bg = 'Green')
    val3 = Label(gui, text=dataDict['500'], fg = 'black', bg = 'Green')
    val4 = Label(gui, text=dataDict['1000'], fg = 'black', bg = 'Green')

    col1.grid(row = 24, column = 0, padx = 3)
    col2.grid(row = 24, column = 1, padx = 3)
    col3.grid(row = 24, column = 2, padx = 3)
    col4.grid(row = 24, column = 3, padx = 3)

    val1.grid(row = 25, column=0, padx = 3)
    val2.grid(row = 25, column=1, padx = 3)
    val3.grid(row = 25, column=2, padx = 3)
    val4.grid(row = 25, column=3, padx = 3)


def task4() :
    global gui
    lb = Label(gui, text = 'Enter Account Number')
    but = Button(gui, text = 'Transaction!', command = Util4, bg = 'black', fg = 'white')

    lb.grid(row=21, column=0)
    e31.grid(row=21, column=1)
    but.grid(row = 22, column = 1)


# Mini Statement : task3

def task3() :
    global gui
    cols = ['Account', 'Deposit', 'Withdraw', 'Old_Password', 'New_Password', 'TimeStamp']
    data = df.tail()        # For Last 5 Transactions

    data_list = [data.columns.values.tolist()] + data.values.tolist()
    t = Table(gui, data_list)
    df.to_csv('Transaction.csv')

# Pin Change : task2 and Util2

def Util2() :
    ac = int(e21.get())
    pwd1 = int(e22.get())
    pwd2 = int(e23.get())

    res = pinChange(ac, pwd1, pwd2)
    verdict = Label(gui, bg='black', fg='yellow', font=5)

    if res == False:
        verdict["text"] = "*** Invalid Input ***"
    else:
        verdict["text"] = "*** Successful Transaction !! ***"
    verdict.grid(row = 14, column = 1)



def task2() :
    global gui
    lb1 = Label(gui, text = 'Enter Account Name : ')
    lb2 = Label(gui, text = 'Enter Old Password : ')
    lb3 = Label(gui, text = 'Enter New Password : ')

    but = Button(gui, text = 'Transaction!', font = 3, command = Util2, bg = 'black', fg = 'white')

    lb1.grid(row = 10, column = 0)
    e21.grid(row = 10, column = 1)
    lb2.grid(row = 11, column = 0)
    e22.grid(row = 11, column = 1)
    lb3.grid(row = 12, column = 0)
    e23.grid(row = 12, column = 1)

    but.grid(row = 13, column = 1)

# Fund Transfer : Task1 and Util1

def Util1() :
    c1 = int(e1.get())
    pwd = int(e2.get())
    ac2 = int(e3.get())
    amt = int(e4.get())
    res = fundTransfer(c1, ac2, amt, pwd)
    verdict = Label(gui, bg = 'black', fg = 'yellow', font = 5)
    if res == False :
        verdict["text"] = "*** Invalid Input ***"
    else :
        verdict["text"] = "*** Successful Transaction !! ***"
    verdict.grid(row = 9, column = 1)

def task1() :
    #print("hello1")
    global gui
    lb1 = Label(gui, text = 'Enter Card Number : ')

    lb2 = Label(gui, text = 'Enter Password : ')
    lb3 = Label(gui, text = 'Enter Account Number :')
    lb4 = Label(gui, text = 'Enter Amount : ')

    but = Button(gui, text = 'Transaction!', font = 3, command = Util1, bg = 'black' , fg = 'white')

    lb1.grid(row = 4, column = 0, sticky = 'w', pady = 2)
    lb2.grid(row=5, column = 0, sticky = 'w', pady = 2)
    e1.grid(row=4, column = 1, sticky = 'w', pady = 2)
    e2.grid(row=5, column = 1, sticky = 'w', pady = 2)
    lb3.grid(row = 6, column = 0, sticky = 'w', pady = 2)
    e3.grid(row = 6, column = 1, sticky = 'w', pady = 2)
    lb4.grid(row = 7, column = 0, sticky = 'w', pady = 2)
    e4.grid(row = 7, column = 1, sticky = 'w', pady = 2)
    but.grid(row = 8, column = 1)

# These are the Part of GUI for Labels and Buttons widgets


label1 = Label(gui, text = ' 1.Fund Transfer ',font = 'georgia',  fg = 'Black', bg = 'Orange',  borderwidth = 3, relief="ridge" )
label2 = Label(gui, text = ' 2.Pin Change ', fg = 'Black', bg = 'Orange', font = 'georgia', borderwidth = 3, relief="ridge" )
label3 = Label(gui, text = ' 3.Mini Statement ', fg = 'Black', bg = 'Orange', font = 'georgia', borderwidth = 3, relief="ridge" )
label4 = Label(gui, text = ' 4.Balance Enquiry ', fg = 'Black', bg = 'Orange', font = 'georgia', borderwidth = 3, relief="ridge" )

button1 = Button(gui, text = 'Click', fg = 'yellow', font = ('georgia', 10, 'bold'), command = task1, bg = 'green', borderwidth = 3)
button2 = Button(gui, text = 'Click', fg = 'yellow', font = ('georgia', 10, 'bold'), command = task2, bg = 'green', borderwidth = 3)
button3 = Button(gui, text = 'Click', fg = 'yellow', font = ('georgia', 10, 'bold'), command = task3, bg = 'green', borderwidth = 3)
button4 = Button(gui, text = 'Click', fg = 'yellow', font = ('georgia', 10, 'bold'), command = task4, bg = 'green', borderwidth = 3)

label1.grid(row = 0, column = 0, sticky = 'w', pady = 2, padx = 3)
button1.grid(row = 0, column = 1, sticky = 'w', pady = 2, padx = 3)
label2.grid(row = 1, column = 0, sticky = 'w', pady = 2, padx = 3)
button2.grid(row = 1, column = 1, sticky = 'w', pady = 2, padx = 3)
label3.grid(row = 2, column = 0, sticky = 'w', pady = 2, padx = 3)
button3.grid(row = 2, column = 1, sticky = 'w', pady = 2, padx = 3)
label4.grid(row = 3, column = 0, sticky = 'w', pady = 2, padx = 3)
button4.grid(row = 3, column = 1, sticky = 'w', pady = 2, padx = 3)



e1 = Entry(gui)
e2 = Entry(gui)
e3 = Entry(gui)
e4 = Entry(gui)
e21 = Entry(gui)
e22 = Entry(gui)
e23 = Entry(gui)
e31 = Entry(gui)

gui.mainloop()