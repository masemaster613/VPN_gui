import os, json
from tkinter import *
from tkinter import ttk

def vpn_start():
	o = os.popen('openvpn3 session-start --config=/home/mason/chrx.ovpn').readlines()
	for line in o:
		if line[0:13] == 'Session path:':
			path = line[14:].strip()
	with open('vpn_path.txt', 'w') as f:
		json.dump(path, f)
	get_sessions()

def vpn_stop():
	with open('vpn_path.txt') as f:
		path=json.load(f)
	os.system('openvpn3 session-manage --path='+ path +' --disconnect')
	get_sessions()

def get_sessions(*args):
	sessions = os.popen('openvpn3 sessions-list').readlines()
	if len(sessions) > 2:
		status.set(sessions[6])
	else:
		status.set('Disconnected')


root = Tk()
root.title('My VPN')

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Button(mainframe, text="Start VPN", command=vpn_start).grid(column=1, row=1, sticky=W)
ttk.Button(mainframe, text="Stop VPN", command=vpn_stop).grid(column=3, row=1, sticky=E)
ttk.Button(mainframe, text="Update Status", command=get_sessions).grid(column=2, row=1, sticky=E)

config = StringVar()
ttk.Entry(mainframe, text_variable=config).grid(column=1, row=2, sticky=W)
#uncomment next line and insert path to your ovpn config file
#config.set('config.ovpn')

sessions_frame = ttk.Frame(root)
sessions_frame.grid(column=0, row=1, sticky=(N, W, E, S))

status = StringVar()
ttk.Label(sessions_frame, textvariable=status).grid(column=1, row=1, sticky=E)
get_sessions()

for child in mainframe.winfo_children(): 
	child.grid_configure(padx=5, pady=5)
root.mainloop()
