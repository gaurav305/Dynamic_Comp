from Tkinter import *
import tkMessageBox
from PIL import ImageTk, Image
from compare_XML import *

import os
#class UI

class CompareGUI():
    def __init__(self):
        self.logFile = r'C:\Users\gaurav.saini\Desktop\DynamicFpML\DynamicFpML\DATA\CompareXML.log'
        self.path1 = ''
        self.path2 = ''

    def run_comp(self):

        root = Tk()

        root.geometry('450x325')
        bckgrg = ImageTk.PhotoImage(Image.open("ihs2.jpg"))
        panel = Label(root, image=bckgrg)
        panel.pack(side="top", fill="both", expand="no", )
        root.title("XML Comparer")

        label = StringVar()
        label = "XML Comparer"
        getlabel = Label(root, textvariable=label, text="XML Compare Version 1.2")
        getlabel.pack()

        text = Entry(root, bg='white', width=50)

        text2 = Entry(root, bg='white', width=50)

        button = Button(root, text="Compare XML", command=self.compareNow)
        #self.compareNow()
        button2 = Button(root, text="Load Path", command=lambda: self.Insert(text, text2))

        list = Listbox(root, bg='blue', fg='yellow')

        text.insert(INSERT, r"C:\Users\gaurav.saini\Desktop\DynamicFpML\DynamicFpML\DATA\T#4_176633847-timestamp.xml")
        text.pack()
        text2.insert(INSERT, r"C:\Users\gaurav.saini\Desktop\DynamicFpML\DynamicFpML\DATA\T#6_176633847-timestamp.xml")
        text2.pack()

        button.pack(padx=4, pady=4, side="bottom")
        button2.pack(padx=4, pady=4, side="bottom")

        # result = self.compareNow()



        # list.pack()
        root.mainloop()

    def Insert(self, text, text2):
        self.path1 = text.get()
        self.path2 = text2.get()
        print "Path 1"+ self.path1
        print "Path 2" + self.path2

    # list.insert(END, name)
    # list.insert(END, name2)
    # text2.delete(0, END)
    # text.delete(0, END)

# root = Tk()
# root.geometry('450x325')
# bckgrg= ImageTk.PhotoImage(Image.open("ihs2.jpg"))
# panel = Label(root, image = bckgrg)
# panel.pack(side = "top", fill = "both", expand ="no", )
# root.title("XML Comparer")

    def compareNow(self):
        # tkMessageBox.showinfo("Hello Python", "Hello World")
        CompareXML(self.path1, self.path2, self.logFile)
        log = pathReport
        tkMessageBox.showinfo("SUCCESS", "Compared at " + self.logFile)


# label = StringVar()
# label = "XML Comparer"
# getlabel = Label(root, textvariable=label, text="XML Comparer Version 1.0")
# getlabel.pack()
#
# # p1= Label(root, text="Path 1")
# # p1.grid(row=2, column=1)
# # p2= Label(root, text="Path 2")
# # p2.pack(side="left")
# text = Entry(root, bg='white', width=50)
#
# text2 = Entry(root, bg='white', width=50)
#
# button = Button(root, text="Compare XML", command=Insert)
# button2 = Button(root, text="Load Path", command=lambda: compareNow(path))
#
# list = Listbox(root, bg='blue', fg='yellow')
#
# text.insert(INSERT,"Enter Path 1")
# text.pack()
# text2.insert(INSERT,"Enter Path 2")
# text2.pack()
#
# button.pack(padx=4, pady=4, side="bottom")
# button2.pack(padx=4, pady=4, side="bottom")
# #list.pack()
# root.mainloop()

if __name__ == '__main__':
    obj = CompareGUI()
    obj.run_comp()
    # loc = 'C:\Users\gaurav.saini\Projects\T#4_176633847-timestamp.xml'
    # print os.path.isfile(loc)
