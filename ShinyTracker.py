# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 14:54:05 2022

@author: Caleb

Should be able to select an existing hunt or create a new hunt

Should automatically update counter after each reset

Should save encounter rate after each hunt

Create csv file if it does not exist

"""
from tempfile import NamedTemporaryFile

import shutil
import csv
import time
import pyautogui as pag

from IPython import get_ipython
    

huntname = 'ray'
confidence_pag = 0.80
reset = "reset.png"
isreset = True

def updateFile():
    """
    Update the SR count of the current hunt and print the count to console

    Returns
    -------
    None.

    """
    fields = ['Name','SR']
    filename = 'hunt.csv'
    tempfile = NamedTemporaryFile(mode='w', delete = False)
    
    #get_ipython().magic('clear')
    print("\033[H\033[J") 
    
    with open(filename, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile,fieldnames = fields)
        writer = csv.DictWriter(tempfile, fieldnames = fields)
        for row in reader:
            if row['Name'] == str(huntname):
               
                print('Current Hunt: ',row['Name'])
                print('# of SR: ', int(row['SR']) + 1)
                row['SR'] = int(row['SR']) + 1 
            row = {'Name': row['Name'],'SR': row['SR']}  
            writer.writerow(row)          
    shutil.move(tempfile.name,filename)
    
def checkForImg(pic):
    """
    Checks if the supplied image is currently also on screen

    Parameters
    ----------
    pic : string
        pic will be the name of the image being looked for on screen

    Returns
    -------
    bool
        returs true if image exists.

    """
    pic_loc = pag.locateCenterOnScreen(pic, confidence = confidence_pag)
    if pic_loc == None:
        return False
    return True
    
def waitForReset():
    """
    Keeps looping until img not found, then loops until image is found

    Returns
    -------
    None.

    """
    #print('Waiting for reset')
    srcount = 0
    while srcount < 3:
        #print('checking for not being on homescreen')
        if checkForImg(reset):
            srcount = 0
        else:
            srcount += 1
            isreset = False
    while isreset == False:
        #print ('checking again for homescreen')
        #print (checkForImg(reset))
        if checkForImg(reset) == True:
            isreset = True
    
while True:
    #print('before wait')
    waitForReset()
    #print('before update')    
    updateFile()
    time.sleep(25)





