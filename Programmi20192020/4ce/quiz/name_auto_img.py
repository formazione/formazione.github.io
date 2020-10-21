names = {
  "Agresta" : "Agr",
  "Chirico" : "Chi",
  "Cona" : "Con",
  "Cuda" : "Cud",
  "DAgosto" : "DAg",
  "DiNola" : "DiN",
  "Filosa" : "Fil",
  "Mariosa" : "Mar",
  "Mazzeo" : "Maz",
  "Merola" : "Mer",
  "Pandullo" : "Pan",
  "Paolino" : "Pao",
  "Papa" : "Pap",
  "Petrone" : "Pet",
  "Ruggiero" : "Rug",
  "Savino" : "Sav",
  "Vassallo" : "Vas",
  "Volpe" : "Vol",
        }

for img in images:
  for name in names:
    os.rename(img, name + ".png")