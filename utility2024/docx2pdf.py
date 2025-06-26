import os
import glob
import comtypes.client
from PyPDF2 import PdfMerger


def docxs_to_pdf():
    """Converts all word files in pdfs and append them to pdfslist"""
    word = comtypes.client.CreateObject('Word.Application')
    pdfslist = PdfMerger()
    x = 0
    for f in glob.glob("*.docx"):
        input_file = os.path.abspath(f)
        output_file = os.path.abspath("demo" + str(x) + ".pdf")
        # loads each word document
        doc = word.Documents.Open(input_file)
        doc.SaveAs(output_file, FileFormat=16+1)
        doc.Close() # Closes the document, not the application
        pdfslist.append(open(output_file, 'rb'))
        x += 1
    word.Quit()
    return pdfslist

def joinpdf(pdfs):
    """Unite all pdfs"""
    with open("result.pdf", "wb") as result_pdf:
        pdfs.write(result_pdf)

def main():
    """docxs to pdfs: Open Word, create pdfs, close word, unite pdfs"""
    pdfs = docxs_to_pdf()
    joinpdf(pdfs)

main()