#Inputs
buffer=3

# Importing the libraries
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('maxPain.csv')

dataset=dataset.replace('-',0)
dataset[['CallOI']]=dataset['CallOI'].astype(str).astype(int)
dataset[['PutOI']]=dataset['PutOI'].astype(str).astype(int)

n=dataset['STRIKE PRICE'].count()
callWorth=[0]*n
putWorth=[0]*n

#Calculate PutLoss

for i in range(n):
    if i<n-1:
        for j in range(i+1,n):
            putWorth[i]=putWorth[i]+((dataset.iloc[[j],[1]].values[0][0]-dataset.iloc[[i],[1]].values[0][0])*dataset.iloc[[j],[2]].values[0][0])     

#Calculate CallLoss
       
for i in range(n):
    if i>0:
        for j in range(i):
            callWorth[i]=callWorth[i]+((dataset.iloc[[i],[1]].values[0][0]-dataset.iloc[[j],[1]].values[0][0])*dataset.iloc[[j],[0]].values[0][0])
            
#Adding to dataset
            
dataset['CallLoss']=callWorth      
dataset['PutLoss']=putWorth
dataset['TotalLoss']=dataset['CallLoss']+dataset['PutLoss']      

#Max Pain

maxPainIndex = dataset[['TotalLoss']].idxmin().values[0]
maxPain = dataset.iloc[[maxPainIndex],[1]].values[0][0]
bufferHigh = maxPain+(maxPain*(buffer/100))
bufferLow = maxPain-(maxPain*(buffer/100))

#Plotting MaxPain

dataset.plot(kind='bar',x='STRIKE PRICE',y='TotalLoss')

#Output

print('Maximum Pain = '+str(bufferLow)+'<'+str(maxPain)+'<'+str(bufferHigh))

#PCR
pcr=dataset['PutOI'].sum()/dataset['CallOI'].sum()
print('Put Call Ratio = '+str(pcr))

put=dataset.nlargest(5, ['PutOI']).iloc[:,[1,2]]  
call=dataset.nlargest(5, ['CallOI']).iloc[:,[0,1]] 