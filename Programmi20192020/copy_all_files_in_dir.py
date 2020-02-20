# copy file

import shutil
from glob import glob

src = "H:\\avatars\\5bs\\"
filedacopiare = glob(src + "*.PNG")
print(filedacopiare)
dest = "H:\\formazione.github.io\\formazione.github.io\\Programmi20192020\\text_5bs\\"
for f in filedacopiare:
    f = f.split("\\")[3]
    print(f)
    shutil.copyfile(src + f, f"{dest}{f}")
    print("copied" + f)

