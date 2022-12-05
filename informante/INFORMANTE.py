from tkinter import *
import os, fnmatch, shutil
import subprocess
from zipfile import ZipFile
from os import remove
import requests


#PARAMETROS

release = 3

#dropbox path
dropbox_path = r'Dropbox'
tmp_path = r'Temp'

#linux
if os.name != 'nt':
	weasis_path = r'/opt/weasis/bin/Weasis'

#windows
else:
	weasis_path = r'c:\\Program Files\\Weasis\\Weasis.exe'

#patron de archivo que se va a mostrar en la lista de estudios
pattern = "*.zip"



def checkForUpdates():
	URL = 'https://raw.githubusercontent.com/alencas/python/main/informante/release'

	try:
		response = requests.get(URL)

		lastRelease = int( response.text )

		if(  lastRelease > release ):

			URL = 'https://raw.githubusercontent.com/alencas/python/main/informante/INFORMANTE.py'

			response = requests.get(URL)

			open("INFORMANTE.py", "wb").write(response.content)

			return True
		else:
			return False

	except OSError:
		print('Algo salio mal!') 

def onClose():
	
	#borro temporales
	for files in os.listdir(tmp_path):
		path = os.path.join(tmp_path, files)
		try:
			shutil.rmtree(path)
		except OSError:
			os.remove(path)

	ws.destroy()

def click():
    for i in listbox.curselection():
        filename = listbox.get(i)        
        listbox.activate(i)


    # loading the temp.zip and creating a zip object
    with ZipFile("./"+dropbox_path+"/"+filename, 'r') as zObject:

        zObject.extractall(path="./"+tmp_path+"/"+filename+"/")

    subprocess.call([weasis_path, str("./"+tmp_path+"/"+filename+"/") ])
    
def Scankey(event):
	val = event.widget.get()
	print(val)
	
	if val == '':
		data = contacts
	else:
		data = []
		for item in contacts:
			if val.lower() in item.lower():
				data.append(item)					
	Update(data)

def Update(data):
	listbox.delete(0, 'end')
	# put new data
	for item in data:
		listbox.insert('end', item)


#inicio
if( checkForUpdates() ):
	print ('Se actualizó la versión del programa! Por favor vuelva a ingresar.')
	exit()

#creo el lienzo de la app
ws = Tk()
ws.title('Ultimos Estudios Subidos a Dropbox')
ws.geometry('620x400')

#creo la caja de input y le atacho la funcion de busqueda
entry = Entry(ws,width=80,font=('Arial 20'))
entry.pack(padx=5, pady=15, side=TOP)
entry.bind('<KeyRelease>', Scankey)

# Creo scrollbar
scrollbar = Scrollbar(ws)
scrollbar.pack(side = RIGHT, fill = BOTH)

#creo listbox
listbox = Listbox(ws,width=80, height=10, font=('Arial 18'),yscrollcommand=scrollbar.set)
#uso la scroll
scrollbar.config(command=listbox.yview)
listbox.pack()



#cargo los datos en la lista
contacts = []
for path in os.listdir(dropbox_path):
    # check if current path is a file
        if os.path.isfile(os.path.join(dropbox_path, path)):
            if fnmatch.fnmatch(path, pattern):
                contacts.append(str(path))

# add data to the treeview
listbox.insert(END, *contacts )

boton = Button(ws, text = "Abrir", width = 10, height=5, font=('Arial 18'), command=click)
boton.pack(side = BOTTOM)

#al cerrar ventana
ws.protocol("WM_DELETE_WINDOW", onClose)

ws.mainloop()
