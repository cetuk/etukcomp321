#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 11:33:22 2024

@author: charlesetuk
"""
'''Question 1'''
#Importing libraries
import pandas as pd
import numpy as np

classics = pd.read_csv('1980sClassics.csv') #Reading in the file as a csv

valencebyyear = classics.groupby('Year').mean('Valence')['Valence'] #Grouping by valence, and summarizing by mean
valencebyyear.to_csv('average_valence_per_year.csv') #Outputing to csv file



'''Question 2'''
def mins_to_sec(time): #Creating a function to convert minutes to seconds
    seconds = 0
    time = time.split(':')
    seconds += int(time[0])*60
    seconds += int(time[1])
    return seconds

classics['Duration'] = classics['Duration'].apply(mins_to_sec) #Applying the function to each entry

#Assigning song length categories by # of seconds
classics['Length'] = ['<1 min' if x < 60 else 
                      '1-3 min' if 60 <= x < 180 else 
                      '3-5 min' if 180 <= x <= 300  else 
                      '>5 min' for x in classics['Duration']]


classicsduration = classics.sort_values(by = 'Duration', ascending = True) #Sorts by duration
bysonglength = classicsduration.set_index('Length')
bysonglength.to_csv('top_5_danceability.csv') #Outputting file

'''Question 3'''
#Getting artists with 5 songs in a category and creating a separate object
artiststop5 = classics.groupby('Artist')['Artist'].count()
artiststop5 = artiststop5[artiststop5 >= 5]
classicsfiltered = classics[classics['Artist'].isin(artiststop5.index)] #Filters original dataset based on if the artist has 5 songs

#Creating variables for mode being 1 or mode being 2 and creates new table
classicsfiltered['Mode0'] = np.where(classicsfiltered['Mode'] == 0, 1, 0)
classicsfiltered['Mode1'] = np.where(classicsfiltered['Mode'] == 1, 1, 0)
modeset = classicsfiltered[['Artist','Mode0','Mode1']]

#Groups by artist, produces the Mode #s
bymode = modeset.groupby('Artist').sum()
bymode['Song Count'] = bymode['Mode0'] + bymode['Mode1'] #Gets the song count
finalmode = bymode[['Song Count','Mode0','Mode1']] 
finalmode.to_csv('mode_count.csv') #Outputs to csv



'''Question 4'''
#Gets the popularity mean grouped by year (odds and evens)
oddyears = classics[classics['Year'] % 2 == 1].groupby('Year')['Popularity'].mean()
evenyears = classics[classics['Year'] % 2 == 0].groupby('Year')['Popularity'].mean()

#Sorts by popularity
oddyears = oddyears.sort_values(ascending = False)
evenyears = evenyears.sort_values(ascending = False)

#Appends the two tables together
oddsandevens = pd.concat([evenyears, oddyears], keys=['Even Years', 'Odd Years'])
oddsandevens.to_csv('even_odd.csv') #Outputs to csv


'''Question 5'''
#Creating function to create a tempo name variable based on the BPM
def tempo_groups(tempo):
    if 60 <= tempo < 70:
        return "Adagio"
    elif 70 <= tempo < 80:
        return "Andante"
    elif 80 <= tempo < 100:
        return "Moderato"
    elif 100 <= tempo < 110:
        return "Allegretto"
    elif 120 <= tempo < 156:
        return "Allegro"
    elif 156 <= tempo < 168:
        return "Vivace"
    elif 168 <= tempo < 200:
        return "Presto"
    elif tempo >= 200:
        return "Prestissimo"

#Applying the categorization function to the table
classics['Tempo Group'] = classics['Tempo'].apply(tempo_groups)

#Grouping by tempo group and artist and getting the song count
bytempo = classics.groupby(['Tempo Group', 'Artist']).count()['Tempo'].reset_index(name='Number of Tracks')

#Creating function to get the top two songs per tempo group
def toptwo(tempogroup):
    return tempogroup.nlargest(2, 'Number of Tracks')

#Applying the function to the sorted tempo table
artistsbytempo = bytempo.groupby('Tempo Group').apply(toptwo).reset_index(drop = True)
artistsbytempo = artistsbytempo[['Artist', 'Tempo Group', 'Number of Tracks']] #Reorganizes the table by artist, group, song count
artistsbytempo.to_csv('tempo_binned.csv') #Outputs to csv











