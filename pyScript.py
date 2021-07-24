#Test task for automatisation ANSYS calculus
#developed by Chetyrbok Ivan 01/2019
#changed 07/2021
#i_ingar@mail.ru ***** github.com/fraIoann

import os
import re

#Updating and wrtiting output file function
def updater():
	P4 = Parameters.CreateParameter(IsOutput=False, DisplayText="PT0/P0")
	
	for row in Data:
		#Get WD\B parameters
		PIn = Parameters.GetParameter(Name = "P1")
		POut = Parameters.GetParameter(Name = 'P2')
		MFIn = Parameters.GetParameter(Name = 'P3') 
		logFile.write('Parameters were gotten \n')
	
		#Rewriting parameters
		PIn.Expression = str(row[0])
		POut.Expression = str(row[1])
		P4.Expression = str(row[0]/row[1])
		DP = Parameters.CreateDesignPoint()
		DP.SetParameterExpression(Parameter=PIn, Expression=PIn.Expression)
		
		#Updating
		Session = UpdateAllDesignPoints(DesignPoints=[DP])
	
		#Cheking update
		MF = str(MFIn.Value)
		MF = MF.split()
		Out = [PIn.Expression, POut.Expression, P4.Expression, MF[0]]
		
		#Writing Output data
		with open(Path + '\OutData.txt', 'a') as f:
			f.writelines('%s, ' % row for row in Out)
			f.write('\n')
		
	#Making chart for MF and PT0/P0 dependence
	chart = Parameters.CreateParameterVsParameterChart()
	chart.XAxisBottom = P4
	chart.YAxisLeft = Parameters.GetParameter(Name="P3")
	chart.IsBaseDesignPointExcluded = True
			
#Reading initial data and prepearing design points			
def readIn():
	global Data
	with open(Path + '\InData.txt') as f:
	#Reading initial values
		values = f.read().split("\n")
		Data = []
		for key in values:
			value = list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", key)))
			if value != []:
				Data.append(value)
	
	#Forming numerical series for PT0 / P0 to determine intervals for study.
	#Although we do not know what value should be changed, the task has a central symmetry
	#We can suppose that PT0 is varied and P0 - fixed. 
	#In another case we have to swap PT0 and P0 respectively.
	i = 0
	while (1.06+0.09*i)<1.5:
		Data.append([round(Data[0][1]*(1.06+0.09*i), 3), Data[0][1]])
		i += 1
		
	#Writing log
	logFile.write('Initial data is PT0 = ' + str(Data[0][0])+', P0 = '+str(Data[0][1]) + '\n')
	#Return parameter series
	return Data

# Open a log file to record script progress 
Path = 'D:\ANSYS Inc\Projects'
logFile = open(Path + '\Test_Task_v1.txt','w')
logFile.write('Processing project in ' + Path + '\n')  

# Project open
Open(FilePath = Path + '\Test_Task_v1.wbpj')
logFile.write('Project opened \n')

readIn()

updater()

#Closing log	
logFile.close()

#Saving and rewriting final analisys results for Post-CFD
Save(FilePath = Path + '\Test_Task_v1_out.wbpj', Overwrite=True)