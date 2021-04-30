from tkinter import *
from PIL import Image, ImageTk

root = Tk()

f = Frame(root)

bkgd = ImageTk.PhotoImage(Image.open('Big Board Images/$2000.png').resize((500,500)))

image = Label(f, image=bkgd)
text = Label(f, text="Hello There", font = ("Calibri", 50))
image.pack()
text.place(anchor=N, relx=0.5, rely=0.45)
f.pack()

root.mainloop()