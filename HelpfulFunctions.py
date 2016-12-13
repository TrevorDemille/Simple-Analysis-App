import numpy as np 
import matplotlib.pyplot as plt 
import glob
import os
from pH import *
from Parser import *
#
#Written by Trevor Demille, Summer 2016, Goldner Biophysics Group
"""
	List of functions necessary/helpful in the analysis of Fluorimeter and Dynamic Light Scattering data.
	Data is all taken to either be in the CSV or TXT format.
	Some conditions on the plotting of data such as the concentrations, iterations, and legends must be maually
		edited in the code here.

	A copy of this file as well as the Parser.py an pH.py python files must be saved in the program files directory where
		the master storage for local python libraries is kept. (ie C_drive-->Program Files-->Python2.7)
"""

#Function to import and parse out data from text files
def loadData(fileName, fileNum):
	#fileName must be of the format: "directory/subdirectory/*.txt" where .txt is the matching 
	#glob is going to find and from which it will choose which files to import. This must be the ending of a filename,
	#not some random part of the filename, and fileNum is the number of files in the directory
	path1 = 'C:/Users/tdemille/Desktop/UMA/Sublime/Python/Text Files for pH'
	inputPath = os.path.join(path1, fileName)
	#
	all_txts = glob.iglob(inputPath)
	print(all_txts)
	#
	columnFiles = [None] * fileNum
	counter = 0  #My poor solution to iterating unevenly is counter variables. Ehh...
	for dataFile in all_txts:
		data = np.loadtxt(dataFile)
		#
		columnFiles[counter] = data
		counter=counter+1
	return columnFiles

def solvepH(R,S):
	#For finding individual pH's based on individual inputs of ratio and std dev
	print(get_pH(R,S))
	#
	self.Rentry.delete(0,'end')
	self.Sentry.delete(0,'end')

def parseFile(Dir, File):
	#Parse a CSV file of the full time, intensity, and background data and save as seperate csv files of the desired bkg and intensities
	#for each individually exported group of data, not the session as a whole (D1, D2, etc)
	Parser(Dir, File)
	#

def Indiv_Ratios(D1file,D2file,bkg1,bkg2,cNum,legd,titl):
	#Assign the lengths of columns and rows to a value
	Dcols = len(D1file[0,:])
	Drows = len(D1file[:,0])-1 #rows are always over counted by 1 due to 0-indexing
	rTotal = Drows*10
	bkgCols = len(bkg1[0,:])
	#Set up matrices to store value solved for in the for loop
	D1bkg = [None] * bkgCols
	D2bkg = [None] * bkgCols
	#Take means of background file columns, as there are half the number of background measurements
	#as there are fluorescein intensity measurements. This is just each column's mean value
	for jj in range(bkgCols):
		D1bkg[jj] = np.mean(bkg1[:,jj], dtype=np.float64)
		D2bkg[jj] = np.mean(bkg2[:,jj], dtype=np.float64)
	#Background files must be resized so that every 5 values (assigned to each concentration) can be taken for a mean
	D1bkg = np.array(D1bkg)
	D1meanBkg = np.mean(D1bkg.reshape(-1,5), axis=1)
	D2bkg = np.array(D2bkg)
	D2meanBkg = np.mean(D2bkg.reshape(-1,5), axis=1)
	#Set up counters so the loop ahead can keep all the indexes on track, and set up empty matrices
	ratTot = Dcols*Drows
	ratios = np.array([])
	D1use = np.array([])
	D2use = np.array([])
	bkgIndex = 0
	count = 1
	countr = 0
	countT = 0
	#
	#Loop to subtract the background from D1 & D2, and to solve for ratios of each concentration mean.
	for cc in range(Dcols):
		if count % 10 == 1:
			bkgIndex = bkgIndex+1
		for rr in range(Drows):
			D1use = np.append(D1use, (D1file[rr,cc]-D1meanBkg[bkgIndex-1]))
			D2use = np.append(D2use, (D2file[rr,cc]-D2meanBkg[bkgIndex-1]))
			result = (D1use[countT+countr]-D2use[countT+countr]) / (D1use[countT+countr]+D2use[countT+countr])
			ratios = np.append(ratios, result)
			#
			countr = countr+1
			countT = cc*Drows
		countr = 0
		count = count+1
	#Split up the ratio values by concentration
	val2 = 1
	sub_RatList = [None]*cNum
	sub_RatRange = [None]*cNum
	ratList = [None]*cNum
	ratRange = [None]*cNum
	for tt in range(cNum):
		sub_RatList[tt] = ratios[(tt*rTotal+1):(val2*rTotal)]
		sub_RatRange[tt] = xrange((tt*rTotal+1),(val2*rTotal))
		ratList[tt] = sub_RatList[tt]
		ratRange[tt] = sub_RatRange[tt]
		val2=val2+1
	#plot everything up individually such that the colors can be changed.
	#The legend has to be manually altered as the concentrations change from measurement to measurement
	colorInd = ['ro','bo','ko','mo','yo','go','co','ro','bo','ko','mo','yo','go','co','ro','bo','ko']
	f, fig1 = plt.subplots()
	for hh in range(cNum):
		fig1.plot(ratRange[hh],ratList[hh],colorInd[hh])
	#fig1.plot(R7,rat7,'yo')
	fig1.set_xlabel('Index', fontsize=15)
	fig1.set_ylabel('Ratio', fontsize=15)
	fig1.set_title(titl, fontsize=18)
	#fig1.legend(['1:100','1:200','1:300','1:400'],numpoints=1,loc=3,frameon=False)
	fig1.legend(['0M','1uM','30uM','100uM','300uM','1mM','3mM','5mM','7.5mM','10mM','15mM','30mM','100mM','200mM'], numpoints=1, loc=4, frameon=False)

def Mean_Ratios(D1file,D2file,bkg1,bkg2,cNum,legd,titl1,titl2):
	#Function to find the means of all the D1 and D2 intensity data found by measuring the 514nm and 550nm
	#emission of fluorescein. This data is taken as 10 sets of 16 measurements for each concentration of surfactant.
	#The mean of each 16 measurements is taken, and the std dev found. the mean of these 10 means is then taken, and
	#its stdev is found.
	Dcols = len(D1file[0,:])
	Drows = len(D1file[:,0])-1
	bkgCols = len(bkg1[0,:])
	#Set up matrices to store data in loop. This isn't the most eficient way, but it works for now.
	D1meanList = [None] * Dcols
	D2meanList = [None] * Dcols
	D1stdList = [None] * Dcols
	D2stdList = [None] * Dcols
	D1bkg = [None] * bkgCols
	D2bkg = [None] * bkgCols
	#Loop to take means and std dev of each column of intensity data
	for i in range(Dcols):
		D1meanList[i] = np.mean(D1file[:,i], dtype=np.float64)
		D2meanList[i] = np.mean(D2file[:,i], dtype=np.float64)
		D1stdList[i] = np.std(D1file[:,i])
		D2stdList[i] = np.std(D2file[:,i])
	#Loop to take mean of background data
	for k in range(bkgCols):
		D1bkg[k] = np.mean(bkg1[:,k], dtype=np.float64)
		D2bkg[k] = np.mean(bkg2[:,k], dtype=np.float64)	
	#I need to take the mean of the first 10 values, then the next 5, then the next 10 and so on, so I must reshape the array
	#by first making them arrays and then spliting them up into fives where the first 2 sets of 5 are intensity data, and 
	#every third set of five values is the corresponding background
	D1bkg = np.array(D1bkg)
	D1meanbkg = np.mean(D1bkg.reshape(-1,5), axis=1)
	D2bkg = np.array(D2bkg)
	D2meanbkg = np.mean(D2bkg.reshape(-1,5), axis=1)
	D1meanList = np.array(D1meanList)
	D1mean = np.mean(D1meanList.reshape(-1,10), axis=1)
	D2meanList = np.array(D2meanList)
	D2mean = np.mean(D2meanList.reshape(-1,10), axis=1)
	D1stdList = np.array(D1stdList)
	D1std = np.mean(D1stdList.reshape(-1,10), axis=1)
	D2stdList = np.array(D2stdList)
	D2std = np.mean(D2stdList.reshape(-1,10), axis=1)
	#Correct intensity data for the background and add the std devs in quadriture
	CorD1 = D1mean-D1meanbkg
	CorD2 = D2mean-D2meanbkg
	D1sqr = np.power(D1std,2)
	D2sqr = np.power(D2std,2)
	DstdAdd = np.sqrt(D1sqr+D2sqr)
	#More matrices
	DstdRat = [None] * cNum
	ratio = [None] * cNum
	topE = [None] * cNum
	botE = [None] * cNum
	#Loop to find the ratio and its errorbars above and below based on the number of iterations or solute concentrations (Cnum)
	for j in range(cNum):
		ratio[j] = (CorD1[j]-CorD2[j]) / (CorD1[j]+CorD2[j])
		topE[j] = np.power((DstdAdd[j] / (CorD1[j]+CorD2[j])),2)
		botE[j] = np.power((DstdAdd[j] / (CorD1[j]-CorD2[j])),2)
		DstdRat[j] = np.sqrt(topE[j] + botE[j])*abs(ratio[j])
	print('\n')
	print('Ratios\n')
	print(ratio)
	print('\n')
	print('Standard Deviations\n')
	print(DstdRat)
	print('\n')
	#
	R = len(ratio)
	pHresults = [None] * R
	devR = [None] * R
	devL = [None] * R
	#Loop to use the get_pH script written by Kieran to find the probabilistic pH and save outputs as printable strings
	#Errorstate gets rid of inevitable errors which accompany values not supported by the ratio curve found in the calibration 
	for kk in range(R):
		with np.errstate(divide='ignore', invalid='ignore'):
			result = get_pH(ratio[kk],DstdRat[kk],plot=False)
		pHresults[kk] = result[0]
		devL[kk] = result[1]
		devR[kk] = result[2]
	#These are to be changed each time new data is taken and used to reflect the concentrations and spot check values
	concList = [0.00001,0.001,0.01,0.03,0.1,0.3,1,3,5,7,10,30,100,200,0.00001,0.001,0.03,0.1,0.3,1,3,5,7.5,10,15,30,100,200] #29 concentrations
	#concPlot = [0.001,0.3,30]
	#repResults = [results[15],results[15],results[15]]

	print('\n')
	print('pHs\n')
	print(pHresults)
	print('\n')
	print('Lower pH std. deviations\n')
	print(devL)
	print('\n')
	print('Upper pH std. deviations\n')
	print(devR)
	print('\n')
	print('Concentrations\n')
	print(concList)
	print('\n')
	#Set up for plotting as subplots so I can add things on top if I do spot checks later.
	f, fig = plt.subplots()
	plt.xscale('log')
	f2, fig2 = plt.subplots()
	plt.xscale('log')
	#If statement for the repeating of old points to check accuracy 
	Repeat=False
	if Repeat==True:
		fig.errorbar(concPlot,ratio[14:cNum],DstdRat[14:cNum], fmt='ro', linewidth=1.5)
		fig2.errorbar(concPlot,repResults,yerr=[devL[14:cNum], devR[14:cNum]], fmt='ro', linewidth=1.5)
	#xScale is changed every time new data is taken. Could add to GUI at some point?
	fig.errorbar(concList[0:14],ratio[0:14],DstdRat[0:14], fmt='bo', linewidth=1.5, label='Repeated Series')
	fig.errorbar(concList[14:cNum],ratio[14:cNum],DstdRat[14:cNum], fmt='r^', linewidth=1.5, label='Original Series')
	fig.set_xlim([0.000001,1000])
	fig.set_xlabel('Concentration (%)', fontsize=15)
	fig.set_ylabel('Ratio', fontsize=15)
	fig.set_title(titl1, fontsize=18)
	plt.grid()
	#
	fig2.errorbar(concList[0:14],pHresults[0:14],yerr=[devL[0:14], devR[0:14]], fmt='k^', linewidth=1.5, label='Repeated Series')
	fig2.errorbar(concList[14:cNum],pHresults[14:cNum],yerr=[devL[14:cNum], devR[14:cNum]], fmt='r^', linewidth=1.5, label='Original Series')
	fig2.set_xlabel('Concentration (%)', fontsize=15)
	fig2.set_ylabel('pH', fontsize=15)
	fig2.set_xlim([0.000001,1000])
	fig2.set_title(titl2, fontsize=18)
	#plt.grid()
	#
	#if legd != '': fig.legend(numpoints=1)
	fig.legend(numpoints=1, loc=2)
	#fig2.legend(numpoints=1, loc=2)
	

def plot_Gen(e1,e2,e3,e4,e5,e6,e7,e8,L2,eColor):
	#Function to plot general data given a text file of columns
	datalist = np.loadtxt(e1)
	rowTot = len(datalist[:,0])
	#Set up plots
	fig, ax0 = plt.subplots()
	#Assign each column assuming a certain organization to x, y, and std dev
	xCol = datalist[:,e2]
	yCol = datalist[:,e3]
	stdCol = datalist[:,e4]
	#If statements to decide if color should be changed mid way through the columns to signify some change in condition of the data
	if eColor != '':
		if e4 != '':
			ax0.errorbar(xCol[0:eColor],yCol[0:eColor],stdCol[0:eColor],fmt='k^')
			ax0.errorbar(xCol[eColor:rowTot],yCol[eColor:rowTot],stdCol[eColor:rowTot],fmt='ko')
		else:
			ax0.plot(xCol,yCol,'k^')
			ax0.plot(xCol,yCol,'ko')
	else:
		if e4 != '':
			stdCol = datalist[:,e4]
			ax0.errorbar(xCol,yCol,stdCol,fmt='k^',linewidth=1.5)
		else:
			ax0.plot(xCol,yCol,'bo')
		#
	if e5 != '' and L2 == '':
		ax0.legend([e5], numpoints=1)
	if e5 != '' and L2 != '':
		ax0.legend([e5,L2], numpoints=1)
	ax0.set_xlabel(e6, fontsize=15)
	ax0.set_ylabel(e7, fontsize=15)
	ax0.set_title(e8, fontsize=18)

def mean_Gen(meanFile,Leg,xLab,yLab,Titl):
	meanData = np.loadtxt(meanFile)
	cols = len(meanData[0,:])
	rows = len(meanData[:,0])
	xscale = range(1,cols+1)
	#Matrices!
	meanVal = [None] * cols
	stdVal = [None] * cols
	for i in range(cols):
		meanVal[i] = np.mean([meanData[:,i]], dtype=np.float64)
		stdVal[i] = np.std([meanData[:,i]])
	#Concentration values subject to manual change in the code
	concent = [2,1,0.5,0.1]
	f, ax1 = plt.subplots()
	ax1.errorbar(concent,meanVal,stdVal,fmt='ko',linewidth=1.5)
	plt.xscale('log')
	ax1.set_xlabel(xLab, fontsize=18)
	ax1.set_ylabel(yLab, fontsize=18)
	ax1.set_title(Titl, fontsize=15)
	ax1.set_xlim(0.05,3)
	#throws error if a blank legend is assigned occasionally. 
	if Leg != '':
		ax1.legend([Leg], numpoints=1)