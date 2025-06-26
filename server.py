import tkinter as tk
import os

''' per vedere memo.html
in locale lancia questo programma, server.py,
e poi localhost:8000 su Chrome
'''


# py -m http.server
print("Sei qui:")
print(os.getcwd())


def lanciaserver():
	os.system("py server2.py")
	import http.server



root = tk.Tk()
root.title("LANCIA SERVER E LOCALHOST")
root.geometry("600x200+800+500")
b1 = tk.Button(root,
	text="Lancia il server",
	font="Arial 20",
	command=lanciaserver)
b1.pack()


