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
	def __init__(self, master, imageSrc, width=600, **kwargs):

		self.imageSrc = imageSrc
	
		# load image
		w = width
		h = int(imageSrc.shape[0] / imageSrc.shape[1] * width)

		# resize image and generate it as tk image
		cv_image = cv2.resize(imageSrc, (w,h))
		pil_image = Image.fromarray(cv_image)
		tk_image = ImageTk.PhotoImage(pil_image)

		# create canvas
		tk.Canvas.__init__(self, master, width=w, height=h, *kwargs)

		# insert image
		self.create_image(0,0, anchor=tk.NW, image=tk_image)
		self.image = tk_image #image should be stored otherwise it is delete by garbage
		
	
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
	# Event raised on mouse clic event
	def mouseClic(self, event):
		
		self.create_image(0,0, anchor=tk.NW, image=self.image) # redraw image

		# draw lines for showing selection
		self.create_line(0, event.y, self["width"], event.y, width=1, fill="#ffffff")
		self.create_line(event.x, 0, event.x, self["height"], width=1, fill="#ffffff")

		if hasattr(self, "onMouseClic"): self.onMouseClic(event.x, event.y)


def main():

	from tkinter import filedialog as fd

	FILENAME = fd.askopenfilename()
	IMG = cv2.cvtColor(cv2.imread(FILENAME), cv2.COLOR_BGR2RGB)
	print(IMG)
	def PRINT_MOUSE_CLIC(x, y): print("clic:", x, y)

	win = tk.Tk()

	canvas = ImageCanvas(win, IMG)
	canvas.enableMouseClic(PRINT_MOUSE_CLIC)
	canvas.pack()

	win.mainloop()


if __name__ == "__main__":
	main()