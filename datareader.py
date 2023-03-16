import data

''' GUI


[title]			[edit][delete]
[paragraf]		[edit][delete]
[link]			[edit][delete]


[save]

'''

print(data.data[0])

def is_title(data):
	''' checks if there is 1 data in the list: is a title '''
	if len(data) == 1:
		return True

def is_paragraph(data):
	''' checks if there are 2 data and the first item is "p" in the list: is a title '''
	if len(data) == 2 and data[0] == "p":
		return True

def test():
	global data

	for num, data in enumerate(data.data):
		if is_title(data):
			print(num, "\n\nTitolo:", data, True)
			# create a label (title) with the title
		else:
			if is_paragraph(data):
				# create label (paragrafh)
				print(num, "paragrafo:", data, True)
			else:
				# create entry widget to change the data
				print(num, "LINK:", data, True)

test()