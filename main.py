#!/usr/bin/env python
# coding: utf-8


import tkinter as tk
from tkinter import filedialog as fd
from PIL import Image, ImageTk
import cv2


from GUI.ImageCanvas import ImageCanvas
from GUI.ImageCanvasInfos import ImageCanvasInfos


class App(tk.Tk):
	
	def __init__(self):
		
		tk.Tk.__init__(self)
		self.canvas = None
		
	
	def clear(self):
		
		if self.canvas:
			self.canvas.destroy()
			self.canvas = None

			self.canvasInfos.destroy()
			self.canvas = None


	def newTP(self):

		self.clear()


	def openImage(self):

		filename = fd.askopenfilename()
		
		if filename != "":

			self.clear()
			
			image = cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2RGB)

			self.canvas = ImageCanvas(self)
			self.canvas.pack(fill=tk.BOTH, expand=True)

			self.canvasInfos = ImageCanvasInfos(self, self.canvas)
			self.canvasInfos.pack()

			self.canvas.setImage(image)
			self.canvas.setMouseClicEvent(lambda x,y: self.canvasInfos.display())


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
	win.title("ImageryVirtualTP")
	win.mainloop()


	
########################################################################################################
if __name__ == "__main__":
	main()

from Zvi import ZviReader, ZviBytesToArray, print_progressbar

#file = "C:/Users/Anthony/Documents/file.zvi"
file = "E:/Imagerie/TP virtuel/file.zvi"
n, images = ZviReader.load(file)

import numpy as np
import cv2


w = 1384
h = 1036

for i in range(n):
	pixels = images[i][-w*h*2:]
	images[i] = np.frombuffer(pixels, dtype=np.uint16).reshape((h,w)).astype(np.float)
	images[i][...] /= 4096

	print_progressbar(i, n-1)


key = 0
i = 0
while key != ord('a'):

	cv2.imshow("", cv2.resize(images[i], (640,480)))
	key = cv2.waitKey(1)

	if key == ord('d'):
		i = min(n-1, i+1)
	if key == ord('q'):
		i = max(0, i-1)

cv2.destroyAllWindows()