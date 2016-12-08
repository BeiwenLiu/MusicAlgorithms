#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 23:35:49 2016

@author: Beiwen Liu
"""
from music21 import *

c = converter.parse('./ChopinNocturneOp9No2.xml') # Get Info from Original Sheet
sc = stream.Score(id="MainScore") # New Stream

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
    #c = converter.parse('./ChopinNocturneOp9No2.xml') # Get Info from Original Sheet
    #sc = stream.Score(id="MainScore") # New Stream
    
    melody = stream.Part(id="part0") # Melody part
    chord1 = stream.Part(id="part1") # Chord part
    
    findAllMeasuresWithinParts(c.parts[0],c.parts[1],chord1,melody)
    """
    timeSignature = c.parts[0].measure(1).getContextByClass('TimeSignature') #Get Time Signature
    keySignature = c.parts[1].measure(1).getContextByClass('KeySignature') #Get Key Signature
    
    #melody.timeSignature = timeSignature
    #melody.keySignature = keySignature
    #chord1.keySignature = keySignature
    #chord1.timeSignature = timeSignature
    #sc.timeSignature = timeSignature
    #sc.keySignature = keySignature
    
    m1 = stream.Measure(number=1)
    m1.keySignature = keySignature
    m1.timeSignature = timeSignature
    m1.append(note.Note('C'))
    m2 = stream.Measure(number=2)
    m2.append(note.Note('D'))
    melody.append([m1,m2])
    
    m11 = stream.Measure(number=1)
    m11.keySignature = keySignature
    m11.timeSignature = timeSignature
    m11.append(note.Note('E'))
    m12 = stream.Measure(number=2)
    m12.append(note.Note('F'))
    chord1.append([m11,m12])
    """
    
    sc.insert(0,melody)
    sc.insert(0,chord1)
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

    
def findAllMeasuresWithinParts(melody,chords,newChord,newMelody):
    
    chordMeasures = chords.measure(0)
    c1 = chordMeasures
    
    melodyMeasures = melody.measure(0)
    m1 = melodyMeasures
    end = False
    counter = 0
    
    melodyList = []
    chordList = []
    while end == False:
        if c1 is None:
            end = True
        else:
            c2 = stream.Measure(number = counter)
            c2.offset = c1.offset
            c2.timeSignature = c1.timeSignature
            m2 = stream.Measure(number = counter)
            m2.offset = m1.offset
            m2.timeSignature = m1.timeSignature
            
            chordArray, singleNoteChord = findAllNotesWithinMeasureChord(c1)
            melodyArray = findAllNotesWithinMeasureMelody(m1)
            c2,m2 = createMashForMeasure(chordArray, melodyArray, singleNoteChord, c2, m2)
            chordList.append(c2)
            melodyList.append(m2)
            c1 = c1.next('Measure')
            m1 = m1.next('Measure')
        counter = counter + 1
    newChord.append(chordList)
    newMelody.append(melodyList)
    
def findAllNotesWithinMeasureChord(measure):
    totalList = []
    totalList2 = []
    for x in measure.flat.recurse():
        if type(x) == chord.Chord:
            totalList.append([x,x.duration,x.offset])
            #print x,x.duration,x.offset
        elif type(x) == note.Note:
            totalList2.append([x,x.duration,x.offset])
    return totalList, totalList2
    
def findAllNotesWithinMeasureMelody(measure):
    totalList = []
    for x in measure.flat.recurse():
        if type(x) == note.Note:
            totalList.append([x.pitch,x.duration,x.offset,x.pitchClass,x])
            #print x.pitch,x.duration,x.offset
    return totalList
                
def createMashForMeasure(chordArray, melodyArray, singleNoteChord, chordM, melodyM):
    print "---"
    if (len(chordArray) > 0 and len(melodyArray) > 0):
        index = 0
        for x in range(0,len(chordArray)): #For each chord in this measure
            start,end = findWindow(chordArray[x][2],chordArray[x][1]) #Find the window size of specific chord
            index, melodyAffected, indexHighest, indexLowest, melodyUnaffected = findMelodiesAffected(start,end,melodyArray,index) #find melodies that are within chord offset + duration
            genScale = findScale(chordArray[x][0], melodyAffected, indexHighest, indexLowest)
            #melodyArray = createNewMelody(chordArray[x], genScale, melodyAffected)
            
    return createNewMeasure(chordArray,chordM,melodyM, singleNoteChord, melodyArray)
  
#def createNewMelody(genChord, genScale, melodyAffected): #This will generate a new melody array using the scales from the chord
    #print genChord,genScale,melodyAffected
              
def createNewMeasure(chordArray,chordM,melodyM,singleNoteChord, melodyArray): #Generate measure here
    print chordArray, len(chordArray)
    numberofSingle = len(singleNoteChord)
    for x in range(0,len(chordArray)):
        if x < numberofSingle:
            chordM.insert(singleNoteChord[x][0])
        print chordArray[x][2]

        chordM.insert(chordArray[x][2],chordArray[x][0])
    for x in range(0,len(melodyArray)):
        melodyM.insert(melodyArray[x][-1])
    return chordM, melodyM
            
def findScale(chord1, melodyArray, indexH, indexL):
    rootNote = str(chord1.findRoot())[:-1] #Beginning to end - 1 to take out the number
    default = False
    if indexH == -1 or indexL == -1:
        default = True
    if chord1.isMajorTriad():
        sc1 = scale.MajorScale(str(rootNote))
    else:
        sc1 = scale.MinorScale(str(rootNote))
    if default:
        genScale = [str(p) for p in sc1.getPitches("{}5".format(rootNote),"{}6".format(rootNote))]
    else:
        genScale = [str(p) for p in sc1.getPitches("{}".format(melodyArray[indexL][0].transpose(-11)),"{}".format(melodyArray[indexH][0].transpose(11)))]
    #print default,chord1,genScale
    #genScale will default to the root scale if no melodies are associated with it
    return genScale
          
def findWindow(offset,duration):
    start = offset
    end = duration.quarterLength + offset
    return start,end


def findMelodiesAffected(start,end,melody,index):
    counter = index
    melodyAffected = []
    melodyUnaffected = []
    highestPitch = 0
    indexHighest = -1
    lowestPitch = 10000
    indexLowest = -1
    tempIndex = 0
    for x in range(index,len(melody)):
        counter = x
        if melody[x][2] >= end: #stop if the offset is past the end offset of chord
            break
        if melody[x][2] >= start and melody[x][2] < end:
            melodyAffected.append(melody[x])
            weight = int(str(melody[x][0])[-1]) + melody[x][3]
            if weight < lowestPitch:
                lowestPitch = weight
                indexLowest = tempIndex
            if weight > highestPitch:
                highestPitch = weight
                indexHighest = tempIndex
            tempIndex = tempIndex + 1
        else:
            melodyUnaffected.append(melody[x])
    return counter, melodyAffected, indexHighest, indexLowest, melodyUnaffected #return the array here with the counter
        #need to also keep track of pitch so that we can give the range of pitches to findScale
   
        
def practice1():
    sc = stream.Score(id="MainScore")
    n1 = note.Note('G')
    n1.offset = 5
    m1 = stream.Measure()
    #m1.timeSignature = meter.TimeSignature('2/4')
    m1.insert(n1)
    m1.offset = 5
    print n1.offset
    print m1.offset
    #m1.insert(0,n1)
    #print m1.activeSite
    #print n1.activeSite
    sc.insert(m1)
    sc.flat.show()

def pr2(m):
    noa = note.Note('G')
    noa.offset = 5
    noa.duration.type="half"
    m.insert(100,noa)
    
#practice1()
#streamCreate()         
createNewStream()
#findAllMeasures()
#findAllNotesWithinMeasure()
#flatStream()    
#noteattributes()
#reconstruction()
#streamCreate()
#main()   
#findScale()