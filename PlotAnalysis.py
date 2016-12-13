import numpy as np
import matplotlib.pyplot as plt
import Parser as Parser
from pH import *
from HelpfulFunctions import *
from Tkinter import *
#
#Written by Trevor Demille, summer 2016, for Goldner Biophysics Group
"""
	GUI for the purpose of expediting the data analysis process for ratio data, DLS data,
	and pH to ratio calculation. This will plot results for each of the possible analyses. 

	Data files must be in the same directory as the PlotAnalysis.py script.
"""


class myButtons:

	def __init__(self, master):
		frame1 = Frame(master)
		frame1.pack(side=LEFT, fill=Y)
		#Labels
		impLabel = Label(frame1, text='Imports', relief=SUNKEN, fg='white', bg='black')
		labelfont = ('times', 15, 'bold')
		buttonfont = ('times', 14)
		impLabel.config(font=labelfont)
		impLabel.pack(side=TOP, fill=X, expand=YES)
		#Entry selection window
		self.selectImports = Button(frame1, text='Import and Plot General',fg='blue',bd=3, command=self.selectImp)
		self.selectImports.config(width=25, height=3, font=buttonfont)
		self.selectImports.pack(side=TOP, padx=4, pady=2, anchor=W)
		#
		self.meanPlot = Button(frame1, text='Import and Plot Means', fg='blue',bd=3,command=self.meanImp)
		self.meanPlot.config(width=25, height=3, font=buttonfont)
		self.meanPlot.pack(side=TOP, padx=4, pady=2, anchor=W)
		#
		self.ratioBut = Button(frame1, text='Import and Plot Ratio Means',fg='blue', bd=3, command=self.plotRatioM)
		self.ratioBut.config(width=25, height=3, font=buttonfont)
		self.ratioBut.pack(side=TOP, padx=4, pady=2, anchor=W)
		#
		self.phBut = Button(frame1, text='Find pH', fg='blue', bd=3, command=self.ph_GUI)
		self.phBut.config(width=25, height=3, font=buttonfont)
		self.phBut.pack(side=TOP, padx=4, pady=2, anchor=W)
		#
		self.parsBut = Button(frame1, text='Parse CSV File', fg='blue', bd=3, command=self.parseGUI)
		self.parsBut.config(width=25, height=3, font=buttonfont)
		self.parsBut.pack(side=TOP, padx=4, pady=2, anchor=W)

	def parseGUI(self):
		root5 = Tk()
		root5.title('Parse CSV File')
		frameRoot = Frame(root5)
		#
		Label1 = Label(root5, text='Input CSV File Directory:')
		Label1.grid(row=0, column=0, padx=3, sticky=W)
		Label2 = Label(root5, text='Input CSV File Name:')
		Label2.grid(row=1, column=0, padx=3, sticky=W)
		#
		self.pEntry1 = Entry(root5, bd=4)
		self.pEntry1.grid(row=0, column=1)
		self.pEntry2 = Entry(root5, bd=4)
		self.pEntry2.grid(row=1, column=1)
		#
		self.pButton = Button(root5, text='Import File', fg='blue', command=self.parseIt)
		self.pButton.config(width=15)
		self.pButton.grid(row=1, column=2, padx=3)

	def ph_GUI(self):
		root4 = Tk()
		root4.title('pH Calculator')
		frameRoot = Frame(root4)
		#
		Label1 = Label(root4, text='Input Ratio:')
		Label1.grid(row=0, column=0, padx=3, sticky=W)
		Label2 = Label(root4, text='Input Ratio Std. Dev.:')
		Label2.grid(row=1, column=0, padx=3, pady=5, sticky=W)
		#
		self.Rentry = Entry(root4, bd=4)
		self.Rentry.grid(row=0, column=1)
		self.Sentry = Entry(root4, bd=4)
		self.Sentry.grid(row=1, column=1, pady=5)
		#
		self.impBut1 = Button(root4, text='Import Ratio Data', fg='blue', command=self.solvepH_setup)
		self.impBut1.config(width=15)
		self.impBut1.grid(row=1, column=2, padx=3)

	def parseIt(self):
		Dir = self.pEntry1.get()
		File = self.pEntry2.get()
		parseFile(Dir,File)
		self.pEntry1.delete(0,'end')
		self.pEntry2.delete(0,'end')

	def solvepH_setup(self):
		R = self.Rentry.get()
		S = self.Sentry.get()
		solvepH(R,S)

	def plotRatioM(self):
		#GUI setup for taking means of fluorimeter ratio emission data taken at 514 & 550 nm.
		#GUI allows the input of text file titles for intensities, backgrounds, and plot axis labels
		root3 = Tk()
		root3.title('Intensity Ratio Data')
		frameRoot = Frame(root3)
		#
		labelR = Label(root3, text='Input D1 File to Import:')
		labelR.grid(row=0, column=0, padx=3, sticky=W)
		labelD2 = Label(root3, text='Input D2 File to Import:')
		labelD2.grid(row=1, column=0, padx=3, pady=5, sticky=W)
		labelB1 = Label(root3, text='Input D1 bkg File:')
		labelB1.grid(row=2, column=0, padx=3, pady=5, sticky=W)
		labelB2 = Label(root3, text='Input D2 bkg File:')
		labelB2.grid(row=3, column=0, padx=3, pady=5, sticky=W)
		labelR2 = Label(root3, text='Legend Text:')
		labelR2.grid(row=4, column=0, padx=3, pady=5, sticky=W)
		LabelR3 = Label(root3, text='pH Plot Title:')
		LabelR3.grid(row=5, column=0, padx=3, pady=5, sticky=W)
		labelR4 = Label(root3, text='Ratio Plot Title:')
		labelR4.grid(row=6, column=0, padx=3, pady=5, sticky=W)
		labelC = Label(root3, text='Concentration Values:')
		labelC.grid(row=0, column=2, padx=3, pady=5, sticky=W)
		#
		self.entryRD1 = Entry(root3, bd=4)
		self.entryRD1.grid(row=0, column=1)
		self.entryRD2 = Entry(root3, bd=4)
		self.entryRD2.grid(row=1, column=1, pady=5)
		self.entrybkg1 = Entry(root3, bd=4)
		self.entrybkg1.grid(row=2, column=1, pady=5)
		self.entrybkg2 = Entry(root3, bd=4)
		self.entrybkg2.grid(row=3, column=1, pady=5)
		self.entryR2 = Entry(root3, bd=4)
		self.entryR2.grid(row=4, column=1, pady=5)
		self.entryR3 = Entry(root3, bd=4)
		self.entryR3.grid(row=5, column=1, pady=5)
		self.entryR4 = Entry(root3, bd=4)
		self.entryR4.grid(row=6, column=1, pady=5)
		self.concNum = Spinbox(root3, from_=0, to=10, width=5, bd=3)
		self.concNum.grid(row=1, column=2, padx=3)
		#
		self.impButR = Button(root3, text='Import for Mean', fg='blue', command=self.getRatioM)
		self.impButR.config(width=15)
		self.impButR.grid(row=5, column=2, padx=3)
		#
		#Allow for the individual ratios to be examined from each file. 
		self.impButR2 = Button(root3, text='Import Individual', fg='blue', command=self.getRatioI)
		self.impButR2.config(width=15)
		self.impButR2.grid(row=4, column=2, padx=3)
		#
		self.runIt = Button(root3, text='Plot Entry', command=self.runCode)
		self.runIt.config(width=15)
		self.runIt.grid(row=6, column=2, padx=3)

	def Ratio_Entry_Delete(self):
		#Clear out inputs after each function taking entries has been successfully completed.
		self.entryRD1.delete(0,'end')
		self.entryRD2.delete(0,'end')
		self.entrybkg1.delete(0,'end')
		self.entrybkg2.delete(0,'end')
		self.entryR2.delete(0,'end')
		self.entryR3.delete(0,'end')
		self.entryR4.delete(0,'end')

	def getRatioI(self):
		#Load in entry information and open text files
		E1 = np.loadtxt(self.entryRD1.get())
		E2 = np.loadtxt(self.entryRD2.get())
		E3 = np.loadtxt(self.entrybkg1.get())
		E4 = np.loadtxt(self.entrybkg2.get())
		E5 = self.concNum.get()
		if E5 != '':
			E5 = int(str(self.concNum.get()))
		E6 = self.entryR2.get()
		E7 = self.entryR4.get()
		#
		Indiv_Ratios(E1,E2,E3,E4,E5,E6,E7)
		#
		self.Ratio_Entry_Delete()	
		
	def getRatioM(self):
		#Load in entry information and open text files
		E1 = np.loadtxt(self.entryRD1.get())
		E2 = np.loadtxt(self.entryRD2.get())
		E3 = np.loadtxt(self.entrybkg1.get())
		E4 = np.loadtxt(self.entrybkg2.get())
		E5 = self.concNum.get()
		if E5 != '':
			E5 = int(str(self.concNum.get()))
		E6 = self.entryR2.get()
		E7 = self.entryR4.get()
		E8 = self.entryR3.get()
		#
		Mean_Ratios(E1,E2,E3,E4,E5,E6,E7,E8)
		#
		self.Ratio_Entry_Delete()

	def selectImp(self):
		root1 = Tk()
		root1.title('Plotting Data Imports')
		frameRoot = Frame(root1)
		#
		label1 = Label(root1, text='Input File to Import:')
		label1.grid(row=0, column=0, padx=3, sticky=W)
		label2 = Label(root1, text='Column Index for X-axis Data:')
		label2.grid(row=1, column=0, padx=3, pady=5, sticky=W)
		label3 = Label(root1, text='Column Index for Y-axis Data:')
		label3.grid(row=2, column=0, padx=3, pady=5, sticky=W)
		label4 = Label(root1, text='Column Index for Std. Dev.:')
		label4.grid(row=3, column=0, padx=3, pady=5, sticky=W)
		labelColor = Label(root1, text='First Row Number for Second Data Set:')
		labelColor.grid(row=4, column=0, padx=3, pady=5, sticky=W)
		label5 = Label(root1, text='First Legend Text:')
		label5.grid(row=5, column=0, padx=3, pady=5, sticky=W)
		label6 = Label(root1, text='Second Legend Text:')
		label6.grid(row=6, column=0, padx=3, pady=5, sticky=W)
		label7 = Label(root1, text='X-axis Label:')
		label7.grid(row=7, column=0, padx=3, pady=5, sticky=W)
		label8 = Label(root1, text='Y-axis Label:')
		label8.grid(row=8, column=0, padx=3, pady=5, sticky=W)
		label9 = Label(root1, text='Plot Title:')
		label9.grid(row=9, column=0, padx=3, pady=5, sticky=W)
		#
		self.entry1 = Entry(root1, bd=4)
		self.entry1.grid(row=0, column=1)
		self.entry2 = Entry(root1, bd=4)
		self.entry2.grid(row=1, column=1, pady=5)
		self.entry3 = Entry(root1, bd=4)
		self.entry3.grid(row=2, column=1, pady=5)
		self.entry4 = Entry(root1, bd=4)
		self.entry4.grid(row=3, column=1, pady=5)
		self.entryColor = Entry(root1, bd=4)
		self.entryColor.grid(row=4, column=1, pady=5)
		self.entry5 = Entry(root1, bd=4)
		self.entry5.grid(row=5, column=1, pady=5)
		self.entryL2 = Entry(root1, bd=4)
		self.entryL2.grid(row=6, column=1, pady=5)
		self.entry6 = Entry(root1, bd=4)
		self.entry6.grid(row=7, column=1, pady=5)
		self.entry7 = Entry(root1, bd=4)
		self.entry7.grid(row=8, column=1, pady=5)
		self.entry8 = Entry(root1, bd=4)
		self.entry8.grid(row=9, column=1, pady=5)
		#
		self.impBut1 = Button(root1, text='Import', fg='blue', command=self.getInput1)
		self.impBut1.grid(row=0, column=3, sticky=N)
		#
		self.runIt = Button(root1, text='Plot Entries', command=self.runCode)
		self.runIt.grid(row=9, column=3, padx=3, pady=5, sticky=E)

	def getInput1(self):
		e1 = self.entry1.get()
		e2 = self.entry2.get()
		e3 = self.entry3.get()
		e4 = self.entry4.get()
		e5 = self.entry5.get()
		e6 = self.entry6.get()
		e7 = self.entry7.get()
		e8 = self.entry8.get()
		L2 = self.entryL2.get()
		eColor = self.entryColor.get()
		if eColor != '':
			eColor = int(str(self.entryColor.get()))
		#
		plot_Gen(e1,e2,e3,e4,e5,e6,e7,e8,L2,eColor)
		#
		self.entry1.delete(0,'end')
		self.entry2.delete(0,'end')
		self.entry3.delete(0,'end')
		self.entry4.delete(0,'end')
		self.entry5.delete(0,'end')
		self.entry6.delete(0,'end')
		self.entry7.delete(0,'end')
		self.entry8.delete(0,'end')
		self.entryL2.delete(0,'end')
		self.entryColor.delete(0,'end')

	def meanImp(self):
		root2 = Tk()
		root2.title('Mean Data Imports')
		frameRootM = Frame(root2)
		#
		labelM = Label(root2, text='Input File to Import:')
		labelM.grid(row=0, column=0, padx=3, sticky=W)
		labelM2 = Label(root2, text='Legend Text:')
		labelM2.grid(row=1, column=0, padx=3, pady=5, sticky=W)
		labelM3 = Label(root2, text='X-axis Label:')
		labelM3.grid(row=2, column=0, padx=3, pady=5, sticky=W)
		labelM4 = Label(root2, text='Y-axis Label:')
		labelM4.grid(row=3, column=0, padx=3, pady=5, sticky=W)
		labelM5 = Label(root2, text='Plot Title:')
		labelM5.grid(row=4, column=0, padx=3, pady=5, sticky=W)
		#
		self.entryM = Entry(root2, bd=4)
		self.entryM.grid(row=0, column=1)
		self.entryM2 = Entry(root2, bd=4)
		self.entryM2.grid(row=1, column=1, pady=5)
		self.entryM3 = Entry(root2, bd=4)
		self.entryM3.grid(row=2, column=1, pady=5)
		self.entryM4 = Entry(root2, bd=4)
		self.entryM4.grid(row=3, column=1, pady=5)
		self.entryM5 = Entry(root2, bd=4)
		self.entryM5.grid(row=4, column=1, pady=5)
		#
		self.impButM = Button(root2, text='Import', fg='blue', command=self.getMean)
		self.impButM.grid(row=0, column=2, padx=3, sticky=W)
		#
		self.runIt = Button(root2, text='Plot Entry', command=self.runCode)
		self.runIt.grid(row=4, column=2, sticky=W)
		
	def getMean(self):
		meanFile = self.entryM.get()
		Leg = self.entryM2.get()
		xLab = self.entryM3.get()
		yLab = self.entryM4.get()
		Titl = self.entryM5.get()
		#
		mean_Gen(meanFile,Leg,xLab,yLab,Titl)
		#
		self.entryM.delete(0,'end')
		self.entryM2.delete(0,'end')
		self.entryM3.delete(0,'end')
		self.entryM4.delete(0,'end')
		self.entryM5.delete(0,'end')
	
	def runCode(self):
		plt.show()

#Establish, title, and loop the main window until the program is manually quit.
root = Tk()
root.title('Data Plotter')
obj = myButtons(root)
root.mainloop()







