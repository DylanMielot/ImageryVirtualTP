#!/usr/bin/env python
# coding: utf-8


import tkinter as tk
from PIL import Image, ImageTk
import cv2


########################################################################################################
# Widget for displaying an image and interact with mouse
# Insert image in a canvas
class ImageCanvas(tk.Canvas):
	

	####################################################################################################
	# Constructor
	# Initialise inherited canvas and insert image
	def __init__(self, master, **kwargs):

		# create canvas
		tk.Canvas.__init__(self, master, *kwargs)
		self.bind('<Configure>', self.onResize)
		self.bind("<Button-1>", self.mouseClic)
		
		self.onMouseClic = None
		self.selected = [-1, -1]
	
	####################################################################################################
	# Set the image to use
	def setImage(self, src_image):

		self.src_image = src_image

		self.displayImage(src_image)
		if self.selected != [-1, -1]:
			self.setLines(self.selected[0], self.selected[1])


	####################################################################################################
	# Set and display image
	def displayImage(self, src_image):

		# set dimensions
		w = self.winfo_width()
		h = self.winfo_height()

		# image transforms
		cv_image = cv2.resize(src_image, (w,h))
		pil_image = Image.fromarray(cv_image)
		# tk image must be stored otherwise it is deleted by garbage
		self.tk_image = ImageTk.PhotoImage(master=self.master, image=pil_image)

		# draw
		self.create_image(0,0, anchor=tk.NW, image=self.tk_image)


	####################################################################################################
	# draw lines for showing selection
	def setLines(self, x, y):

		x = int(x * self.winfo_width())
		y = int(y * self.winfo_height())

		self.create_line(0, y, self.winfo_width(), y, width=1, fill="#ffffff")
		self.create_line(x, 0, x, self.winfo_height(), width=1, fill="#ffffff")


	####################################################################################################
	# Enable the mouse clic event to be captured
	def setMouseClicEvent(self, onMouseClic):
		if onMouseClic:
			self.onMouseClic = onMouseClic
		

	####################################################################################################
	# Event raised on mouse clic event
	def mouseClic(self, event):

		#calc pos on source image
		self.selected[0] = event.x / self.winfo_width()
		self.selected[1] = event.y / self.winfo_height()

		self.displayImage(self.src_image)
		self.setLines(self.selected[0], self.selected[1])

		# if a function is waiting for this event, call it
		if self.onMouseClic:
			x = int(self.selected[0] * self.src_image.shape[1])
			y = int(self.selected[1] * self.src_image.shape[0])
			self.onMouseClic(x, y)


	####################################################################################################
	# Resize image
	# called for the 1st display at root mainloop
	def onResize(self, event):

		self.displayImage(self.src_image)
		if self.selected != [-1, -1]:
			self.setLines(self.selected[0], self.selected[1])


########################################################################################################
def main():

	from tkinter import filedialog as fd

	win = tk.Tk()

	# should be launched after main app window init
	FILENAME1 = fd.askopenfilename()
	FILENAME2 = fd.askopenfilename()

	IMG1 = cv2.cvtColor(cv2.imread(FILENAME1), cv2.COLOR_BGR2RGB)
	IMG2 = cv2.cvtColor(cv2.imread(FILENAME2), cv2.COLOR_BGR2RGB)
	def PRINT_MOUSE_CLIC(x, y): print("clic:", x, y)
	def SET_IMG1(): canvas.setImage(IMG1)
	def SET_IMG2(): canvas.setImage(IMG2)

	canvas = ImageCanvas(win)
	canvas.setMouseClicEvent(PRINT_MOUSE_CLIC)
	canvas.setImage(IMG1)
	canvas.pack(fill=tk.BOTH, expand=True)

	b1 = tk.Button(win, text="display img 1", command=SET_IMG1)
	b1.pack()

	b2 = tk.Button(win, text="display img 2", command=SET_IMG2)
	b2.pack()

	win.mainloop()


########################################################################################################
if __name__ == "__main__":
	main()