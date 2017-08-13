#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 07:05:26 2017

@author: vishnuhari
"""

import random
import datetime
import csv
import time
import numpy as np


# I can set to 1000 by default, but can be any number.
numberofsamples=1000

#These are the banners which we expect to show, a total of 10 banners
imagekey=['birch','armani','chloe','prada','espirit','Doir','Diesel','Vougue','Zara','Boss']

#List of locations where am generating the banners. The second parmeter is more like
#weightage which we will use to get a true, false value when creating random click events
locations = {'london': 0.4,
        'newyork':0.4,
      'losangeles':0.35
      }

banners = list()
banner=""

#Using a random seed.
#random.seed(random.randrange(2,10))

loclist = list(locations.keys())

#A set of variables required to track the clicks by location.
london ,newyork,losangeles =0,0,0

#Initialize the variables to collect a click and noclick by location 
falselondon,truelondon,falsenewyork,truenewyork,falselosangeles,truelosangeles=0,0,0,0,0,0

totfalse,tottrue =0,0

#randomly I pick a banner from the list
for customer in range(1,numberofsamples+1):
    location = random.choice(loclist)
    
    #here we just take location, a random image
    #the epoch value of time, a sequence of customerid,
    # a random true, false value based on the value of the locations
    #key we initialized
    banner= (location,
             random.choice(imagekey),
             time.time(),
             customer,np.random.rand() < locations[location])
    
    #Get total false vs true based on value generated in banner variable
    if banner[4]==False:
        totfalse +=1
    else:
        tottrue +=1    
    
    #For the location, track if banner value is clicked or not clicked
    #this way i will know by location, how many clicked and not clicked
    if location == 'london':
        london +=1
        if banner[4]==False:
            falselondon+=1
        else:
            truelondon+=1
    elif location == 'newyork':
        newyork+=1
        if banner[4]== False:
            falsenewyork += 1
        else:
            truenewyork += 1
    else:
        losangeles+=1
        if  banner[4]==False:
            falselosangeles += 1
        else:
            truelosangeles += 1

    banners.append(banner)
   
    
#Write this to file which we can use to read and see if thompson sampling can improve.    
with open('clickdata.csv', mode='w') as wfile:
    writer = csv.writer(wfile, delimiter=',')
    for item in banners:
        writer.writerow([item[1],item[0],item[4],
                     item[3],item[2],
                     time.time()])

print(totfalse)
print(tottrue)

print("Overall London:{}-{}-{}, Newyork:{}-{}-{}, LA:{}-{}-{}".format(london,truelondon,falselondon,
                                                                              newyork,truenewyork,falsenewyork,
                                                                              losangeles,truelosangeles,falselosangeles))
print("Total clicks - {}".format(truelosangeles+truelondon+truenewyork))
