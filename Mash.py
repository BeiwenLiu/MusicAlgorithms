#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 23:35:49 2016

@author: Beiwen Liu
"""
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
    #measure.notes[x].offset for offset
    for x in range(0,len(measure.notes)):
        print "chord" + str(measure.notes[x].offset)
def determineMelody(measure):
    for x in range(0,len(measure.notes)):
        print "melody" + str(measure.notes[x].offset)

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
        determineMelody(melody.measure(x))
        
def streamCreate():
    c = chord.Chord(['C4','E4','G4'])
    n = note.Note('F#4')
    m = stream.Measure()
    m.append(n)
    m.append(c)
    
    n = stream.Measure()
    n.append(n)
    n.append(c)
    
    
    """
    p1 = stream.Part()
    n2 = note.Note('C6')
    p1.append(n2)
    p2 = stream.Part()
    n3 = note.Note('G6')
    p2.append(n3)"""
    s = stream.Stream()
    
    s.insert(0,m)
    
    
    s.show()
    
def createNewStream():
    c = converter.parse('./ChopinNocturneOp9No2.xml') # Get Info from Original Sheet
    sc = stream.Score() # New Stream
    
    melody = stream.Part() # Melody part
    chord1 = stream.Part() # Chord part
    
    m = stream.Measure() 
    
    timeSignature = c.parts[0].measure(1).getContextByClass('TimeSignature') #Get Time Signature
    keySignature = c.parts[1].measure(1).getContextByClass('KeySignature') #Get Key Signature
    
    melody.timeSignature = timeSignature
    melody.keySignature = keySignature
    chord1.keySignature = keySignature
    chord1.timeSignature = timeSignature
    
    melody.append(m)
    
    findAllMeasuresWithinParts(c.parts[0],c.parts[1])
    
    
    sc.insert(0,melody)
    sc.insert(1,chord1)
    sc.show()
    
def noteattributes():
    c = converter.parse('./ChopinNocturneOp9No2.xml')
    pitch = c.parts[0].measure(1).notes[0].pitch
    duration = c.parts[0].measure(1).notes[0].duration
    offset = c.parts[0].measure(1).notes[0].offset

    print pitch,duration,offset
    
    

def noteCreation(pitch, duration, offset):
    n = note.Note(pitch)
    n.duration = duration
    n.offset = offset
    return n

    
def findAllMeasuresWithinParts(melody,chords):
    chordMeasures = chords.measure(0)
    c1 = chordMeasures
    
    melodyMeasures = melody.measure(0)
    m1 = melodyMeasures
    end = False
    while end == False:
        if c1 is None:
            end = True
        else:
            chordArray = findAllNotesWithinMeasure(c1, "Chord")
            melodyArray = findAllNotesWithinMeasure(m1, "Melody")
            createMashForMeasure(chordArray, melodyArray)
            c1 = c1.next('Measure')
            m1 = m1.next('Measure')
            
def findAllNotesWithinMeasure(measure, whatType):
    totalList = []
    if (whatType == "Chord"):
        for x in measure.flat.recurse():
            if type(x) == chord.Chord:
                totalList.append([x,x.duration,x.offset])
                #print x,x.duration,x.offset
    elif (whatType == "Melody"):
        for x in measure.flat.recurse():
            if type(x) == note.Note:
                totalList.append([x.pitch,x.duration,x.offset,x.pitchClass])
                #print x.pitch,x.duration,x.offset
    return totalList
                
def createMashForMeasure(chordArray, melodyArray):
    print "---"
    if (len(chordArray) > 0 and len(melodyArray) > 0):
        index = 0
        for x in range(0,len(chordArray)): #For each chord in this measure
            start,end = findWindow(chordArray[x][2],chordArray[x][1]) #Find the window size of specific chord
            index, melodyAffected = findMelodiesAffected(start,end,melodyArray,index) #find melodies that are within chord offset + duration
            #findScale(chordArray[x][0], melodyAffected) 

def findScale(chord1):
    rootNote = str(chord1.findRoot())[:-1] #Beginning to end - 1 to take out the number
    
    if chord1.isMajorTriad():
        sc1 = scale.MajorScale(str(rootNote))
    else:
        sc1 = scale.MinorScale(str(rootNote))
    fullScale = [str(p) for p in sc1.getPitches("{}5".format(rootNote),"{}6".format(rootNote))]
          
def findWindow(offset,duration):
    start = offset
    end = duration.quarterLength + offset
    return start,end


def findMelodiesAffected(start,end,melody,index):
    counter = index
    melodyAffected = []
    highestPitch = 0
    lowestPitch = 0
    for x in range(index,len(melody)):
        counter = x
        if melody[x][2] >= end: #stop if the offset is past the end offset of chord
            break
        if melody[x][2] >= start and melody[x][2] < end:
            melodyAffected.append([melody[x][0],melody[x][3]])
            weight = int(str(melody[x][0])[-1]) + melody[x][3]
            print weight
            #next steps -> need to make an array of all melodies affected here
    return counter, melodyAffected #return the array here with the counter
        #need to also keep track of pitch so that we can give the range of pitches to findScale
    

          
createNewStream()
#findAllMeasures()
#findAllNotesWithinMeasure()
#flatStream()    
#noteattributes()
#reconstruction()
#streamCreate()
#main()   
#findScale()