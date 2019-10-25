a = [1,2,3]
for n,x in enumerate(j:=a[:]):
	(j:=j[:]).append(x)
print(j)
print(a)