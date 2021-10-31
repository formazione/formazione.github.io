a = "3?2??"

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

