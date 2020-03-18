#!/usr/bin/env python
# coding: utf-8

import tkinter as tk

win = tk.Tk()
win.attributes('-alpha', 0.0)
win.iconify()

img_w = 512
img_h = 512
screen_w = win.winfo_screenwidth()
screen_h = win.winfo_screenheight()

offsetx = int((screen_w-img_w) / 2)
offsety = int((screen_h-img_h) / 2)

window = tk.Toplevel(win)
window.geometry(f"{img_w}x{img_h}+{offsetx}+{offsety}")
window.overrideredirect(1)

photo = tk.PhotoImage(file="logo.png")

c = tk.Canvas(window, width=img_w, height=img_h)
c.config(bg='#000000')
c.create_image(0,0, anchor=tk.NW, image=photo)
c.pack()

win.after(100, win.quit)
win.mainloop()

from main import *
win.destroy()
main()