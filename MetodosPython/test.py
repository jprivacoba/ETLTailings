import Tkinter
from PIL import ImageTk, Image
import os

root = Tkinter.Tk()
versionwin = Tkinter.Toplevel(root)
img = ImageTk.PhotoImage(Image.open('.\logo\logo_hgi.gif'))
panel = Tkinter.Label(versionwin, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")
root.mainloop()