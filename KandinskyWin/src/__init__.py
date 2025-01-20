from matplotlib import pyplot as plt
from matplotlib import image as mpimg
import mido
from mido import MidiFile, MidiTrack, Message
import numpy as np

plt.title("Root image")
plt.xlabel("time")
plt.ylabel("note")

rootImage = mpimg.imread("C:/Users/Johan/eclipse-workspace/KandinskyWin/johtonic.png")
plt.imshow(rootImage)
plt.show()

imageData = rootImage.tolist()

mid = MidiFile()
trackr = MidiTrack()
trackg = MidiTrack()
trackb = MidiTrack()
mid.tracks.append(trackr)
mid.tracks.append(trackg)
mid.tracks.append(trackb)

tempo = mido.bpm2tempo(120)
trackr.append(mido.MetaMessage('set_tempo', tempo=tempo))
trackg.append(mido.MetaMessage('set_tempo', tempo=tempo))
trackb.append(mido.MetaMessage('set_tempo', tempo=tempo))

notes = [0,127,64,65,67]
duration = 1

l = 0
lineFactor = 127/len(imageData)
goOn = False
lastPitch = 0

messagesArrayR = [[] for _ in range (len(imageData[0])+1)]
messagesArrayG = [[] for _ in range (len(imageData[0])+1)]
messagesArrayB = [[] for _ in range (len(imageData[0])+1)]

for line in imageData:
	nc = 0
	l = l+1
	pitch = int(lineFactor*l)
	
	if pitch == lastPitch:
		goOn = False
		continue
	else:
		goOn = True
		lastPitch = pitch
		if ( False              # if all false, chromatic scale is activated, for other decomment the notes to filter.
		  #or (pitch % 12 == 0) #               C
		  #or (pitch % 12 == 1) #               c#
		  #or (pitch % 12 == 2) #               D
		  #or (pitch % 12 == 3) #               eb
		  #or (pitch % 12 == 4) #               e
		  #or (pitch % 12 == 5) #               f
		  #or (pitch % 12 == 6) #               f#
		  #or (pitch % 12 == 7) #               g
		  #or (pitch % 12 == 8) #               ab
		  #or (pitch % 12 == 9) #               a
		  #or (pitch % 12 == 10)#               bb
		  #or (pitch % 12 == 11) #             H
		  ):
			goOn = False
			continue 
		


	oldVR = 0
	oldVG = 0
	oldVB = 0
			
	for n in line:
		start = 0 #int(nc*duration)
		end = duration #int((nc+1)*duration)


		
		note = [
			int(n[0]*127), 
			int(n[1]*127), 
			int(n[2]*127),
		]

		if(note[0] > 100 ):#filter channel 1 for high velocities
			if(oldVR != note[0]):
					messagesArrayR[nc].append(Message('note_on', note=pitch, velocity=note[0], time=start))
					oldVR = note[0]
		else:					
			messagesArrayR[nc].append(Message('note_off', note=pitch, velocity=64, time=end))	
			
		if(note[1] > 80 and note[1] < 100):#filter channel 2 for medium velocities
			if(oldVG != note[1]):
					messagesArrayG[nc].append(Message('note_on', note=pitch, velocity=note[1], time=start))
					oldVG = note[1]
		else:					
			messagesArrayG[nc].append(Message('note_off', note=pitch, velocity=64, time=end))	

		if(note[2] > 60 and note[1] < 80): #filter channel 3 for lower velocities
			if(oldVB != note[2]):
					messagesArrayB[nc].append(Message('note_on', note=pitch, velocity=note[2], time=start))
					oldVB = note[2]
		else:					
			messagesArrayB[nc].append(Message('note_off', note=pitch, velocity=64, time=end))	
		
		nc = nc+1
	
	if (goOn):
		messagesArrayR[nc].append(Message('note_off', note=pitch, velocity=64, time=end))
		messagesArrayG[nc].append(Message('note_off', note=pitch, velocity=64, time=end))
		messagesArrayB[nc].append(Message('note_off', note=pitch, velocity=64, time=end))
		print(l, end)
	
for message in messagesArrayR:
	trackr.extend(message)
for message in messagesArrayG:
	trackg.extend(message)
for message in messagesArrayB:
	trackb.extend(message)


mid.save('kandsky.mid')