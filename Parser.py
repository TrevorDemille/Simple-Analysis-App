#
#Written by Trevor Demille, summer 2016, for Goldner Biophysics Group
"""
	Parser designed to keep only the intensity data from D1 and D2 data files taken from the fluorimeter
	and put into an excel sheet saved as a csv file.
"""
import numpy as np
#
def Parser(Dir, File):
	directory = Dir
	fileName = File
	fileName = np.append(directory,fileName)
	#
	with open(fileName) as F:
		for line in F:
			A = line.split(',')
			data = A[1::2]
			Str = ','.join(data)

			with open('JustData.csv', 'a+') as F2:
				F2.write(Str)
		#
	with open('JustData.csv', 'r+') as F3:
		for row in F3:
			B = row.split(',')
			B = np.array(B)
			fiveData = B.reshape(-1,5)
			#
			bkg = fiveData[2::3]
			bkgArr = np.concatenate(bkg[:], axis=0)
			bkgStr = ','.join(bkgArr)
			#
			flr1 = fiveData[0::3]
			flr2 = fiveData[1::3]
			flrArray = [None]*len(flr1)
			#
			for kk in range(len(flr1)):
				flrArray[kk] = np.append(flr1[kk],flr2[kk])
			#
			flrArray = np.array(flrArray)
			flrList = np.concatenate(flrArray[:], axis=0)
			flrData = ','.join(flrList)

			with open('IntenData.csv', 'a+') as F4:
				F4.write(flrData)
				F4.write('\n')
				Success1 = True
			with open('BkgData.csv', 'a+') as F5:
				F5.write(bkgStr)
				Success2 = True
	#
	if Success1 == True && Success2 == True:
		print('\n')
		print(Parse Successful)
		print('\n')



