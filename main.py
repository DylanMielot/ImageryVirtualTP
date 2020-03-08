#!/usr/bin/env python
# coding: utf-8


import tkinter as tk
from tkinter import filedialog as fd
from PIL import Image, ImageTk
import cv2

from GUI.ImageCanvas import ImageCanvas


#class ImageCanvas(tk.Canvas):
	
#	def __init__(self, master, imagefile, **kwargs):
	
#		pil_image = Image.open(imagefile)
#		tk_image = ImageTk.PhotoImage(pil_image)

#		tk.Canvas.__init__(self, master, width=pil_image.size[0], height=pil_image.size[1], *kwargs)
#		self.create_image(0,0, anchor=tk.NW, image=tk_image)
#		self.image = tk_image
		
	
#	def select(self, event):
		
#		self.create_image(0,0, anchor=tk.NW, image=self.image)
#		self.create_line(0, event.y, self["width"], event.y, width=1, fill="#ffffff")
#		self.create_line(event.x, 0, event.x, self["height"], width=1, fill="#ffffff")
		
		
class ImageCanvasMeta(ImageCanvas):
	
	def __init__(self, master, imagefile, **kwargs):
		
		self.pos = None

		frame = tk.Frame(master)
		
		ImageCanvas.__init__(self, frame, imagefile, **kwargs)
		ImageCanvas.pack(self)
		
		txt = f"w={self.image.width()}; h={self.image.height()}"
		self.label = tk.Label(frame, text=txt)
		self.label.pack(side=tk.RIGHT)
		
		
	def pack(self, *args, **kwargs):
		
		self.master.pack(*args, **kwargs)
		
	
	def select(self, event):
		
		self.pos = (event.x, event.y)
		
		ImageCanvas.select(self, event)
		self.label["text"] = f"w={self.image.width()}; h={self.image.height()}; x={event.x}; y={event.y}"



class App(tk.Tk):
	
	def __init__(self):
		
		tk.Tk.__init__(self)
		self.canvas = None
		
	
	def clear(self):
		
		if self.canvas:
			self.canvas.destroy()
			self.canvas = None


	def newTP(self):

		self.clear()


	def openImage(self):

		filename = fd.askopenfilename()
		
		if filename != "":

			self.clear()
			
			image = cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2RGB)

			self.canvas = ImageCanvas(self)
			self.canvas.setImage(image)
			self.canvas.setMouseClicEvent(None)
			self.canvas.pack(fill=tk.BOTH, expand=True)


def main():

	win = App()

	menuBar = tk.Menu(win)

	fileMenu = tk.Menu(menuBar)
	fileMenu.add_command(label="New", command=win.newTP)
	fileMenu.add_command(label="Open", command=win.openImage)
	fileMenu.add_command(label="Quit", command=win.destroy)
	menuBar.add_cascade(label="File", menu=fileMenu)

	toolsMenu = tk.Menu(menuBar)
	toolsMenu.add_command(label="Drugs", command=None)
	toolsMenu.add_command(label="Sensors", command=None)
	toolsMenu.add_command(label="Reset", command=None)
	menuBar.add_cascade(label="Tools", menu=toolsMenu)

	graphMenu = tk.Menu(menuBar)
	graphMenu.add_command(label="Records", command=None)
	graphMenu.add_command(label="Show", command=None)
	menuBar.add_cascade(label="Graph", menu=graphMenu)

	win.config(menu=menuBar)
	win.mainloop()

main()

from Zvi import ZviReader, ZviBytesToArray

file = "C:/Users/Anthony/Documents/file.zvi"
#zvi = ZviReader.load(file)

#import numpy as np
#import cv2

#with open("C:/Users/Anthony/Documents/Contents", mode="rb") as file:
##with open("C:/Users/Anthony/Documents/img.16b", mode="rb") as file:
#	data = file.read()

#	w = 1384
#	h = 1036
#	pixels = data[-w*h*2:]

#	img = np.frombuffer(pixels, dtype=np.uint16).reshape((h,w))

#cv2.imshow("", cv2.resize(img*100, (640,480)))
#cv2.waitKey(0)