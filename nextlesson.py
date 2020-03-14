import tkinter as tk
import os


def save(obj, classe):
    
    c4ce = """c4ce = document.getElementById("nextlesson4ce");
c4ce.innerHTML = `<h4>Prossimo incontro on line</h4>--content1--`"""
    c4ce = c4ce.replace("4ce", classe)

    
    newtext = c4ce.replace("--content1--", "<br>".join(obj.get()))
    print(newtext)
    with open("nextlesson{}.js".format(classe), "w", encoding="utf-8") as file:
        print("nextlesson{}.js".format(classe))
        print()
        file.write(newtext)
    return "ok"

def save_all():
    save(list1, "4ce")
    save(list2, "5ce")
    save(list3, "5bs")
    os.startfile("index.html")

root = tk.Tk()
root.geometry("400x400+200+10")
root.title("Select to delete and ctr+s to save")
label = tk.Label(root, text="4ce")
label.pack()
list1 = tk.Variable(value="""lunedì 10.00 - 11.30
mercoledì 10.00 - 11.30
Venerdì 10.30 - 11.30""".splitlines())
text1 = tk.Listbox(root, listvariable=list1, height=5)
text1.pack()


text1.bind("<<ListboxSelect>>", lambda x: text1.delete(tk.ANCHOR))


# 5ce
label = tk.Label(root, text="5ce")
label.pack()
list2 = tk.Variable(value="""lunedì 10.00 - 11.30
mercoledì 10.00 - 11.30
Venerdì 10.30 - 11.30""".splitlines())
text2 = tk.Listbox(root, listvariable=list2, height=5)
text2.pack()

text2.bind("<<ListboxSelect>>", lambda x: text2.delete(tk.ANCHOR))



#5bs
label = tk.Label(root, text="5bs")
label.pack()
list3 = tk.Variable(value="""lunedì 10.00 - 11.30
mercoledì 10.00 - 11.30
Venerdì 10.30 - 11.30""".splitlines())

text3 = tk.Listbox(root, listvariable=list3, height=5)
text3.pack()

text3.bind("<<ListboxSelect>>", lambda x: text3.delete(tk.ANCHOR))


root.bind("<Control-s>", lambda x: save_all())

root.mainloop()
#184 270