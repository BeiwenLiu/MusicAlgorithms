#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 23:35:49 2016

@author: MacbookRetina
"""
import music21
from music21 import *


def switch():
    c = converter.parse('./KL_Rains_of_Castamere.xml')
    c2 = converter.parse('./dreamchaser.xml')
    number = len(c2.parts[1]) #number of measures
    number2 = len(c2.parts[1].measure(4))
    c = c.parts[0].flat
    print c2.parts[1].measure(4).notes[1].duration.type
    print number2
    #s = stream.Score()
    #s.insert(0,c)
    #s.insert(1,c2)
    #s.show()
    
def determineChord(measure):
    for x in range(0,len(measure.notes)):
        print measure.notes[x]
    
def findScale():
    c2 = chord.Chord(['g','e-','b-'])
    rootNote = c2.findRoot()
    print rootNote
    print c2.commonName
    if c2.isMajorTriad():
        sc1 = scale.MajorScale(str(rootNote))
    else:
        sc1 = scale.MinorScale(str(rootNote))
    print [str(p) for p in sc1.getPitches("{}5".format(rootNote),"{}6".format(rootNote))]
           

def main():
    c = converter.parse('./ChopinNocturneOp9No2.xml')
    melody = c.parts[0] #Melody part
    chord = c.parts[1] #Chord part
    measureLength = len(melody) #Number of measures
    print "length: " + str(measureLength)
    for x in range(1,measureLength): #For all measures
        print "index" + str(x)
        if (len(chord.measure(x).notes) == 0 and len(melody.measure(x).notes) == 0):
            break
        determineChord(chord.measure(x))
        
        
 
main()   
#findScale()