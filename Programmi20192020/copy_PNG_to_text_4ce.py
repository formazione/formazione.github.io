# copy file

import shutil
from glob import glob

f = "DApolito Giuliano.PNG"
src = "H:\\avatars\\"
dest = "H:\\formazione.github.io\\formazione.github.io\\Programmi20192020\\text_5bs\\"
# for f in filedacopiare:

shutil.copyfile(src + f, dest + f)

