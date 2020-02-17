# copy file

import shutil


filedacopiare = "Ciardi.PNG Merola.PNG Fluri.PNG Romano.PNG Saja_A.PNG".split()
src = "H:\\avatars\\"
dest = "H:\\formazione.github.io\\formazione.github.io\\Programmi20192020\\text_4ce\\"
for f in filedacopiare:
    shutil.copyfile(src + f, dest + f)

