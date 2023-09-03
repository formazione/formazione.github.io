from datetime import datetime
import os
from pyscript import Element

now = datetime.now()
data = """
Ultimi progetti in progress:
loop6 in D:\\python\\pylatform\\code2
tkinter images
""".splitlines()


display("Today is " + now.strftime("%d/%m/%Y"))
display("Appuntamenti:")
for d in data:
    display(d)



def directory(div):
  divtarget = Element(div)
  text = ""
  for v in dir(divtarget):
    text += v + v.__doc__
  display(text, target=div)

def show(text, div):
  divtarget = Element(div)
  if divtarget.innerHtml == "":
    divtarget.write("Il campo è vuoto")
    divtarget.write(text)
    # directory(div)
  else:
    divtarget.write("")