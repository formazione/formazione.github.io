# copy file

import shutil

formato = ".PNG"
filedacopiare = "Ciardi Merola Fluri Romano Saja_A".split()

for f in filedacopiare:
	shutil.copyfile("H:\\avatars\\" + f + formato, "H:\\formazione.github.io\\formazione.github.io\\Programmi20192020\\text_4ce\\" + f + formato)

