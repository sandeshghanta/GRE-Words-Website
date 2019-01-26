import PyPDF2
file = open('Work Sheet 3.pdf','rb')
pdf = PyPDF2.PdfFileReader(file)
#for page in pdf: https://github.com/0xabu/pdfannots/blob/master/pdfannots.py
print (pdf.getPage(3).extractText())
print (pdf.numPages)
file.close()