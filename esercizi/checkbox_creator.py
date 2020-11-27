import os

def choose():
	folder = "dati"
	files = os.listdir(folder)
	x = enumerate(files)
	counter = 0
	ckbx = ""
	for n,fname in x:
		print(n, fname)
	ch = int(input("choose > "))
	path = os.path.join(folder, os.listdir(folder)[ch])
	with open(path, "r", encoding="utf-8") as file:
		for line in file:
			if line != "\n":
				if counter != 0:
					ckbx = "[ ],"
			else:
				ckbx = ""
				counter = -1
			print(ckbx, line.strip())
			counter += 1
	return choose

ch = choose()

