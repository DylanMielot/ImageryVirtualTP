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
	def __init__(self, master, src_image, **kwargs):

		self.src_image = src_image
		self.selected = [-1, -1]

		# create canvas
		tk.Canvas.__init__(self, master, *kwargs)
		self.bind('<Configure>', self.onResize)

	
	####################################################################################################
	# Enable the mouse clic event to be captured
	def enableMouseClic(self, onMouseClic):
		if onMouseClic: self.onMouseClic = onMouseClic
		self.bind("<Button-1>", self.mouseClic)
		
	
	####################################################################################################
	# Disable the mouse clic event to be captured
	def disableMouseClic(self):
		del self.onMouseClic
		self.bind("<Button-1>", None)


	####################################################################################################
	# Set and display image
	def setImage(self):

		# set dimensions
		w = self.winfo_width()
		h = self.winfo_height()

		# resize image and generate it as tk image
		cv_image = cv2.resize(self.src_image, (w,h))
		pil_image = Image.fromarray(cv_image)

		# tk image must be stored otherwise it is deleted by garbage
		self.tk_image = ImageTk.PhotoImage(master=self.master, image=pil_image)

		# draw
		self.create_image(0,0, anchor=tk.NW, image=self.tk_image)


	####################################################################################################
	# draw lines for showing selection
	def setLines(self, x, y):

		self.create_line(0, y, self.winfo_width(), y, width=1, fill="#ffffff")
		self.create_line(x, 0, x, self.winfo_height(), width=1, fill="#ffffff")


	####################################################################################################
	# Event raised on mouse clic event
	def mouseClic(self, event):
		
		self.setImage()
		self.setLines(event.x, event.y)

		#calc pos on source image
		x = int(event.x / self.winfo_width() * self.src_image.shape[1])
		y = int(event.y / self.winfo_height() * self.src_image.shape[0])

		#save it
		self.selected[0] = x
		self.selected[1] = y

		# if a function is waiting for this event, call it
		if hasattr(self, "onMouseClic"):
			self.onMouseClic(x, y)


	####################################################################################################
	# Resize image
	# called for the 1st display
	def onResize(self, event):

		self.setImage()

		if self.selected != [-1, -1]:
			x = int(self.selected[0] / self.src_image.shape[1] * self.winfo_width())
			y = int(self.selected[1] / self.src_image.shape[0] * self.winfo_height())
			self.setLines(x, y)


def main():

	from tkinter import filedialog as fd

	win = tk.Tk()

	# const
	FILENAME = fd.askopenfilename() # should be launched after main app window
	IMG = cv2.cvtColor(cv2.imread(FILENAME), cv2.COLOR_BGR2RGB)
	def PRINT_MOUSE_CLIC(x, y): print("clic:", x, y)

	canvas = ImageCanvas(win, IMG)
	canvas.enableMouseClic(PRINT_MOUSE_CLIC)
	canvas.pack(fill=tk.BOTH, expand=True)

	win.mainloop()


if __name__ == "__main__":
	main()