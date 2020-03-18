#!/usr/bin/env python
# coding: utf-8


import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox

from PIL import Image, ImageTk
import numpy as np
import cv2
import matplotlib.pyplot as plt
from sklearn import metrics


from ImageCanvas import ImageCanvas
from ImageCanvasInfos import ImageCanvasInfos
from ZviReader import ZviReader, print_progressbar



#############################################################################################
class App(tk.Tk):
	

	#########################################################################################
	def __init__(self):
		
		tk.Tk.__init__(self)
		self.canvas = None
		self.rec = []
	
	#########################################################################################
	def clear(self):
		
		if self.canvas:
			self.canvas.destroy()
			self.canvasInfos.destroy()
			self.canvas = None

		for widget in self.pack_slaves(): widget.destroy()
		for widget in self.grid_slaves(): widget.destroy()


	#########################################################################################
	def newTP(self):

		self.clear()


	#########################################################################################
	def openImage(self):

		self.filename = fd.askopenfilename()
		
		if self.filename == "":
			messagebox.showerror("Information", "Opération annulée")
		if self.filename[-4:] != ".zvi":
			messagebox.showerror("Erreur", "Selectionnez un fichier '.zvi'.")
		else:
			self._askInfos()

	#########################################################################################
	def _loading(self):

		self.clear()
		self.n_frame, self.images = ZviReader.load(self.filename)

		w = self.infos[0]
		h = self.infos[1]

		for i in range(self.n_frame):
			pixels = self.images[i][-w*h*2:]
			self.images[i] = np.frombuffer(pixels, dtype=np.int16).reshape((h,w))

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
			self._show(n)
		def nextf():
			n = min(slider.get()+1, self.n_frame)
			slider.set(n)
			self._show(n)

		button_prev = tk.Button(cont, text="<", command=prevf)
		slider = tk.Scale(cont, from_=0, to=self.n_frame-1, orient=tk.HORIZONTAL, command=self._show)
		frame_counter = tk.Label(cont, text="0")
		button_next = tk.Button(cont, text=">", command=nextf)

		button_prev.grid(row=0, column=0)
		slider.grid(row=0, column=1)
		button_next.grid(row=0, column=2)
		self.canvasInfos.grid(row=0, column=3)

		self._show(0)
			

	#########################################################################################
	def _askInfos(self):

		self.clear()
		
		tk.Label(self, text="resolution x").grid(row=0, column=0, sticky=tk.E)
		tk.Label(self, text="resolution y").grid(row=1, column=0, sticky=tk.E)
		tk.Label(self, text="temps de capture").grid(row=2, column=0, sticky=tk.E)

		res_x = tk.Entry(self)
		res_x.insert(0, "1384")
		res_x.grid(row=0, column=1)

		res_y = tk.Entry(self)
		res_y.insert(0, "1036")
		res_y.grid(row=1, column=1)

		temps = tk.Entry(self)
		temps.insert(0, "2000")
		temps.grid(row=2, column=1)

		def set_infos():
			try:
				self.infos = [
					int(res_x.get()),
					int(res_y.get()),
					int(temps.get()),
					]
				self._loading()
			except ValueError:
				self.infos = -1
				messagebox.showerror("Erreur", "Infos non valides.")

		def cancel():
			self.clear()
			messagebox.showerror("Information", "Opération annulée")

		tk.Button(self, text="Valider", command=set_infos).grid(row=3, column=0)
		tk.Button(self, text="Annuler", command=cancel).grid(row=3, column=1)


	#########################################################################################
	def _show(self, n_frame):

		self.canvas.setImage(self.images[int(n_frame)])
		self.canvasInfos.display()


	#########################################################################################
	def record(self):

		select = self.canvas.getSelection()

		if select:
			x, y = select
			
			i = []
			for image in self.images:
				i.append(image[y,x])

			temps = []
			for n in range(self.n_frame):
				temps.append(self.infos[2]*n/self.n_frame)

			self.rec_pos = (x, y)
			self.rec = [i, temps]

			messagebox.showinfo("Information", "Enregistrement effectué.")

		else:
			messagebox.showerror("Erreur", "Selectionnez une zone à enregistrer.")


	#########################################################################################
	def exportGraph(self):

		if len(self.rec):
			plt.plot(self.rec[1], self.rec[0])
			plt.xlabel('Temps (ms)')
			plt.ylabel('Intensite')
			plt.axis([0, self.infos[2], 0, int(max(self.rec[0])*1.1)])
			plt.title('Intensite en fonction du temps en {}'.format(self.rec_pos))
			plt.show()
		else:
			messagebox.showerror("Erreur", "Enregistrez la zone avant export.")
			

	#########################################################################################
	def auc(self):

		messagebox.showinfo("Calcul AUC", "Mesure de l'AUC : {}".format(metrics.auc(self.rec[1], self.rec[0])))


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
	graphMenu.add_command(label="Record", command=win.record)
	graphMenu.add_command(label="Show", command=win.exportGraph)
	graphMenu.add_command(label="Calc auc", command=win.auc)
	menuBar.add_cascade(label="Graph", menu=graphMenu)

	win.config(menu=menuBar)
	win.title("ImageryVirtualTP")
	win.mainloop()

	return win


	
########################################################################################################
if __name__ == "__main__":
	app = main()