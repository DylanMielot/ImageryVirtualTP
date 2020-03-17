#!/usr/bin/env python
# coding: utf-8


import tkinter as tk
from PIL import Image, ImageTk
import cv2

from ImageCanvas import ImageCanvas
		
		
########################################################################################################
class ImageCanvasInfos(tk.Label):
	
	####################################################################################################
	def __init__(self, master, canvas, **kwargs):
		
		tk.Label.__init__(self, master, **kwargs)

		self.canvas = canvas
		self.display()

	
	####################################################################################################
	def display(self):
		
		dims = self.canvas.getDims()
		select = self.canvas.getSelection()
		pix = self.canvas.getPixel()

		self["text"] = ""
		if dims: self["text"] += f"w={dims[0]}; h={dims[1]}"
		if select: self["text"] += f"; x={select[0]}; y={select[1]}"
		if pix: self["text"] += f"; pixel={pix}"



########################################################################################################
def main():

	from tkinter import filedialog as fd
	#from GUI.ImageCanvas import ImageCanvas

	win = tk.Tk()

	# should be launched after main app window init
	FILENAME1 = fd.askopenfilename()

	IMG1 = cv2.cvtColor(cv2.imread(FILENAME1), cv2.COLOR_BGR2RGB)
	def PRINT_MOUSE_CLIC(x, y):
		canvasInfos.display()
		print("clic:", (x, y), "==", canvas.getSelection(), "; dims:", canvas.getDims())

	canvas = ImageCanvas(win)
	canvas.setMouseClicEvent(PRINT_MOUSE_CLIC)
	canvas.setImage(IMG1)
	canvas.pack(fill=tk.BOTH, expand=True)

	canvasInfos = ImageCanvasInfos(win, canvas)
	canvasInfos.pack()

	win.mainloop()


########################################################################################################
if __name__ == "__main__":
	main()