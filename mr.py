from os import walk
from tkinter import *
import vlc

track = 0

col = ['#FF6666','#FFBB66','#FFFF66','#BBFF66','#66FF66','#66FFBB','#66FFFF','#66BBFF','#6666FF','#9966FF','#FF66FF','#FF66BB']

def update_track():
	l = float(player.get_length())
	if l > 0:
		t = int(1024.0 * float(player.get_time()) / l)
		canvas.coords(progress, 0, 400, t+1, 450)	
	root.after(250, update_track)

def mouseclick(event):    
	global track
	global track_name	
	global player
	x = event.x
	y = event.y
	
	if y >= 400 and y <= 450:
		t = int(player.get_length() * event.x / 1024)
		player.set_time(t)    		

	if x >= 12 and x <= 1012 and y >= 12 and y <= 120:
		chosen_track = int((x - 12) / 10) + int((y - 12) / 10) * 100		
		if chosen_track < len(files):
			track = chosen_track			
			filename_bits = files[track].split('/')
			track_name = filename_bits[len(filename_bits)-1]
			print ('Track {0} selected: {1}.'.format(track+1, track_name))							
			canvas.itemconfigure(text, text=track_name)
			player.stop()
			player = vlc.MediaPlayer(files[track])
			player.play()		

def keypress(event):
	print ('Key pressed {0}'.format(event.char))

root = Tk()

canvas = Canvas(root, width=1024, height=768)
canvas.pack()
canvas.bind('<Button-1>', mouseclick)

canvas.create_rectangle(0, 400, 1023, 450, fill="blue")
progress = canvas.create_rectangle(0, 400, 0, 450, fill="red")
text = canvas.create_text(20, 200, anchor='nw')

musicpath = '/home/steve/Music/'
files = []
for (dirpath, dirnames, filenames) in walk(musicpath):
	for filename in filenames:		
		files.append(dirpath + '/' + filename)	
files.sort()

file_counter = 0
album_counter = 0
last_album = ''
for j in range(0, 12):
	for i in range(0, 100):		
		filename_bits = files[file_counter].split('/')
		trackname_bits = filename_bits[len(filename_bits) - 1].split('-')
		album = trackname_bits[1].strip()
		print (album)
		if album != last_album:
			last_album = album
			album_counter += 1
		c = col[album_counter % len(col)]
		canvas.create_rectangle(12+i*10, 12+j*10, 12+i*10+9, 12+j*10+9, fill=c)
		file_counter += 1		
		if file_counter == len(files):
			break
	if file_counter == len(files):
		break

print ('Found {0} mp3s.'.format(len(files)))

filename_bits = files[track].split('/')
track_name = filename_bits[len(filename_bits)-1]
print ('Track {0} selected: {1}.'.format(track+1, track_name))				
canvas.itemconfigure(text, text=track_name)
player = vlc.MediaPlayer(files[0])
player.play()	

root.after(250, update_track)
root.mainloop()

