import weasyprint

html_file = open('index.html', 'rb')
pdf_file = open('out.pdf', 'wb')

weasyprint.HTML(string=html_file.read()).write_pdf(pdf_file)