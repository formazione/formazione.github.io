#punti_mask

import pickle
import tkinter as tk

file = open("punti.pkl", "rb")
a = pickle.load(file)
file.close()
print(a)


root = tk.Tk()
root.geometry("400x900")
frames = []
entries = []
entriesvar = []
cnt = 0

day = "21.9"

def set_score():
	global entries

	print(entries)

	cnt = 0
	print("adding data to day:")
	print(day)
	for k in a:
		a[k][dayString.get()] = entriesvar[cnt].get()
		cnt += 1
	print(a)
	file = open("punti.pkl", "wb")
	pickle.dump(a, file)
	file.close()


dayString = tk.StringVar()
d = tk.Entry(root, textvariable=dayString, bg="yellow")
d.pack(side="top")

for n in a:
	frames.append(tk.Frame(root).pack(side="top"))
	l = tk.Label(frames[cnt], text=n)
	l.pack(side="top")
	# frames.append(tk.Frame(root).pack(side="top"))
	entriesvar.append(tk.IntVar())
	entries.append(tk.Entry(frames[cnt], textvariable=entriesvar[cnt]).pack(side="top"))
	cnt += 1

for n in entriesvar:
	n.set(0)
button = tk.Button(root, text="Send", command=set_score).pack()
root.mainloop()