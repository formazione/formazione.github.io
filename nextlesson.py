import tkinter as tk
import os
import time

def save(obj, classe):
	
	c4ce = """c4ce = document.getElementById("nextlesson4ce");
c4ce.innerHTML = `<h4>Prossimo incontro on line</h4>--content1--`"""
	c4ce = c4ce.replace("4ce", classe)

	read = obj.get(obj.curselctio())
	newtext = c4ce.replace("--content1--", read)
	print(newtext)
	with open("nextlesson{}.js".format(classe), "w", encoding="utf-8") as file:
		print("nextlesson{}.js".format(classe))
		print()
		file.write(newtext)
	time.sleep(1)
	return "ok"

def save_all():
	save(text1, "4ce")
	save(text2, "5ce")
	save(text3, "5bs")
	os.startfile("index.html")

root = tk.Tk()
root.geometry("400x400+200+10")
label = tk.Label(root, text="4ce")
label.pack()
text1 = tk.Listbox(root, height=5)
text1.pack()
list1 = """lunedì 10.30 - 11.30 - martedì 9.30 - 10.30
mercoledì 12.00 - 13.00
Venerdì 10.30 - 11.30
Sabato 11.00 - 12.00""".splitlines()
for i in list1:
	text1.insert(tk.END, i)
text1.bind("<<ListboxSelect>>", lambda x: text1.delete(tk.ANCHOR))


# 5ce
label = tk.Label(root, text="5ce")
label.pack()
text2 = tk.Listbox(root, height=5)
text2.pack()
list2 = """lunedì 11.30 - 12.30
mercoledì 9.00 - 11.00
Venerdì 11.30 - 12.30
Sabato 10.00 - 11.00""".splitlines()
for i in list2:
	text2.insert(tk.END, i)
text2.bind("<<ListboxSelect>>", lambda x: text2.delete(tk.ANCHOR))



#5bs
label = tk.Label(root, text="5bs")
label.pack()
text3 = tk.Listbox(root, height=5)
text3.pack()
list3 = """lunedì 9.30 - 10.30
martedì 10.30 - 12.30
mercoledì 11.00 - 12.00
Venerdì 9.30 - 10.30""".splitlines()
for i in list3:
	text3.insert(tk.END, i) 
text3.bind("<<ListboxSelect>>", lambda x: text3.delete(tk.ANCHOR))


root.bind("<Control-s>", lambda x: save_all())

root.mainloop()
#184 270