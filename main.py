#!/usr/bin/env python
# coding: utf-8


import tkinter as tk
from tkinter import filedialog as fd
from PIL import Image, ImageTk
import numpy as np
import cv2


from GUI.ImageCanvas import ImageCanvas
from GUI.ImageCanvasInfos import ImageCanvasInfos
from Zvi import ZviReader, ZviBytesToArray, print_progressbar


#############################################################################################
class App(tk.Tk):
	
	#########################################################################################
	def __init__(self):
		
		tk.Tk.__init__(self)
		self.canvas = None
		
	
	#########################################################################################
	def clear(self):
		
		if self.canvas:
			self.canvas.destroy()
			self.canvas = None

			self.canvasInfos.destroy()
			self.canvas = None


	#########################################################################################
	def newTP(self):

		self.clear()


	#########################################################################################
	def openImage(self):

		filename = fd.askopenfilename()
		
		if filename != "":

			self.clear()
			
			self.n_frame, self.images = ZviReader.load(filename)

			w = 1384
			h = 1036
			for i in range(self.n_frame):
				pixels = self.images[i][-w*h*2:]
				self.images[i] = np.frombuffer(pixels, dtype=np.int16).reshape((h,w))
				#self.images[i] /= 4096

				print_progressbar(i, self.n_frame-1)

			self.canvas = ImageCanvas(self)
			self.canvas.pack(fill=tk.BOTH, expand=True)

			cont = tk.Frame(self)
			cont.pack(side=tk.BOTTOM)

			self.canvasInfos = ImageCanvasInfos(cont, self.canvas)
			self.canvas.setMouseClicEvent(lambda x,y: self.canvasInfos.display())

			def prevf():
				n = max(slider.get()-1, 0)
				slider.set(n)
				self.show(n)
			def nextf():
				n = min(slider.get()+1, self.n_frame)
				slider.set(n)
				self.show(n)

			button_prev = tk.Button(cont, text="<", command=prevf)
			slider = tk.Scale(cont, from_=0, to=self.n_frame-1, orient=tk.HORIZONTAL, command=self.show)
			frame_counter = tk.Label(cont, text="0")
			button_next = tk.Button(cont, text=">", command=nextf)

			button_prev.grid(row=0, column=0)
			slider.grid(row=0, column=1)
			button_next.grid(row=0, column=2)
			self.canvasInfos.grid(row=0, column=3)

			self.show(0)


	#########################################################################################
	def show(self, n_frame):

		self.canvas.setImage(self.images[int(n_frame)])
		self.canvasInfos.display()


#############################################################################################
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

	return win


	
########################################################################################################
if __name__ == "__main__":
	app = main()

#from Zvi import ZviReader, ZviBytesToArray, print_progressbar

##file = "C:/Users/Anthony/Documents/file.zvi"
#file = "E:/Imagerie/TP virtuel/file.zvi"
#n, images = ZviReader.load(file)

#import numpy as np
#import cv2


#w = 1384
#h = 1036

#for i in range(n):
#	pixels = images[i][-w*h*2:]
#	images[i] = np.frombuffer(pixels, dtype=np.uint16).reshape((h,w)).astype(np.float)
#	images[i][...] /= 4096

#	print_progressbar(i, n-1)


#key = 0
#i = 0
#while key != ord('a'):

#	cv2.imshow("", cv2.resize(images[i], (640,480)))
#	key = cv2.waitKey(0)

#	if key == ord('d'):
#		i = min(n-1, i+1)
#	if key == ord('q'):
#		i = max(0, i-1)

#cv2.destroyAllWindows()