#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 11:33:22 2024

@author: charlesetuk
"""
'''Question 1'''
import pandas as pd

classics = pd.read_csv('1980sClassics.csv') #Reading in  file
valencebyyear = classics.groupby('Year').mean('Valence') #Grouping by valence summarizing by mean
valencebyyear = valencebyyear['Valence']

valencebyyear.to_csv('valenceoutput.csv') #Outputing to csv

'''Question 2'''
def mins_to_sec(time): #Conversion function
    seconds = 0
    time = time.split(':')
    seconds += int(time[0])*60
    seconds += int(time[1])
    return seconds

classics['Seconds'] = classics['Duration'].apply(mins_to_sec) #Applying function
classics['Duration'] = classics['Seconds']
classics = classics.drop('Seconds', axis=1)
#Assigning length
classics['Length'] = ['<1 min' if x < 60 else '1-3 min' if 60 <= x < 180 else '3-5 min' if 180 <= x <= 300  else '>5 min' for x in classics['Duration']]

classics = classics.sort_values(by = 'Duration', ascending = False)
songlength = classics.set_index('Length')
songlength = songlength.transpose()
#Orienting 

'''Question 3'''
#Getting artists with 5 songs
artists5 = classics.groupby('Artist')['Artist'].count()
artists5 = artists5[artists5 >= 5]
classicsfiltered = classics[classics['Artist'].isin(artists5.index)]


'''Question 4'''
#Filter the dataframe into 2, odds and evens sets
#Group each dataframe by year and summarize by mean popularity
