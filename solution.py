
a = "3?2??"

def count(lst):
	num = 0
	for i in lst:
		if i=="?":
			num += 1
	return num

x = count(a)

pattern = "12"
a = list(a)
pos = 0
for n, i in enumerate(a):
	if i=="?":
		a[n] = pattern[pos]
		pos += 1
		if pos > 1:
			pos = 0
	else:
		pos = 0

a = "".join(a)
print(a)
