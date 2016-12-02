#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 23:35:49 2016

@author: MacbookRetina
"""
import music21
from music21 import *


def main():
    c = converter.parse('./KL_Rains_of_Castamere.xml')
    c2 = converter.parse('./dreamchaser.xml')
    c2 = c2.parts[1].flat
    c = c.parts[0].flat
    s = stream.Score()
    s.insert(0,c)
    s.insert(1,c2)
    s.show()
    
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
    
#main()

findScale()