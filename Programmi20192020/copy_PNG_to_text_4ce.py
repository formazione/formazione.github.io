# copy file

import shutil
from glob import glob
f = input("Name of the file in avatars to copy")
c = input("Name of the class (4ce, 5ce, 5bs")
# f = "DApolito Giuliano.PNG"
src = "H:\\avatars\\"
dest = f"H:\\formazione.github.io\\formazione.github.io\\Programmi20192020\\text_{c}\\"
# for f in filedacopiare:

shutil.copyfile(src + f, dest + f)

