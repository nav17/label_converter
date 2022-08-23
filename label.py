from email import message
from PyPDF2 import PdfFileReader, PdfFileWriter
from tkinter.filedialog import askopenfilename
import os.path
import tkinter as tk
import os
import tkinter.filedialog as fd
import fitz as fz
import numpy as np
from tkinter import messagebox
from PIL import Image


# TODO: 
# open new label file after its made
#  clear labels button to clear list

working = True

root = tk.Tk()
root.title('Label Converter')

root.geometry("400x350")
root.eval('tk::PlaceWindow . center')
root.columnconfigure(0, weight=1)

def OpenFile():
    name = askopenfilename()
    print(name)

file_list = []

def file_chooser():
    files = fd.askopenfilenames(parent=root, title='Choose a File')
    for file in files:
        print("chosen: " + file)
        file_list.append(file)
        lb.insert("end", file)

frame = tk.Frame(root)
#frame.pack()
frame.grid(column=0, row=2, padx=5, pady =5)

menu = tk.Menu(root)
root.config(menu=menu)
filemenu=tk.Menu(menu)
#menu.add_cascade(label="File", menu=filemenu)
#filemenu.add_command(label="Open...", command=OpenFile)
#filemenu.add_command(label="Exit", command=root.quit)
menu.add_command(label="Exit", command=root.quit)

lb = tk.Listbox(frame, width="40")
lb.grid(column=0,row=0)


scrollbarY = tk.Scrollbar(frame)
scrollbarY.config(command=lb.yview)
scrollbarY.grid(column=1,row=0, sticky="ns")
scrollbarX = tk.Scrollbar(frame, orient="horizontal")
scrollbarX.config(command=lb.xview)
scrollbarX.grid(column=0,row=1, sticky="ew")
lb.config(yscrollcommand=scrollbarY.set, xscrollcommand=scrollbarX.set)

def laced_label():
    print(file_list)
    #files = lb.get(0, tk.END)
    #print(files)
    #for file in files:
    #    file = "".join(str(files))
    #    print("a file: " + file)
    newlabel = PdfFileWriter()
    for file in file_list:
        edit=PdfFileReader(open(f'{file}', 'rb'))
        print(file)
        file_dir = os.path.dirname(file)
        file_name = os.path.basename(file)
        print(file_name)

        if file_name.endswith('- Shipping Label.pdf'):
            page = edit.getPage(0)
            page.cropBox.upperLeft = (130, 695)
            page.cropBox.lowerRight = (470, 485)
            page.mediaBox.upperLeft = (130, 695)
            page.mediaBox.lowerRight = (470, 485)
            page.bleedBox.upperLeft = (130, 695)
            page.bleedBox.lowerRight = (470, 485)
            page.artBox.upperLeft = (130, 695)
            page.artBox.lowerRight = (470, 485)
            page.trimBox.upperLeft = (130, 695)
            page.trimBox.lowerRight = (470, 485)
            lacedqr = PdfFileWriter()
            lacedqr.addPage(page)
            lacedqr_path = os.path.join(file_dir, 'lacedqr.pdf')
            Output = open(f'{lacedqr_path}', 'wb')
            lacedqr.write(Output)
            Output.close()
            
            # alias qr code to image
            doc = fz.open(lacedqr_path)
            page = doc.load_page(0)  # number of page
            pix = page.get_pixmap(dpi=300)
            output = os.path.join(file_dir, "outfile.png")
            pix.save(output)
            print("saved qr as image")

            # gamma increase
            im = Image.open(output).convert('L')
            imnp = np.array(im)/255
            gamma=0.2
            new = ((imnp**(1/gamma))*255).astype(np.uint8)
            Image.fromarray(new).save(output)
            print("gamma increased")

            # back to pdf
            doc = fz.open()
            img = fz.open(output)  # open pic as document
            rect = img[0].rect  # pic dimension
            pdfbytes = img.convert_to_pdf()  # make a PDF stream
            img.close()  # no longer needed
            imgPDF = fz.open("pdf", pdfbytes)  # open stream as PDF
            page = doc.new_page(width = rect.width, height = rect.height)  # pic dimension
            page.show_pdf_page(rect, imgPDF, 0)  # image fills the page
            doc.save(lacedqr_path)
            print("saved as new pdf")

            # add qr pdf to print
            qredit=PdfFileReader(open(f'{lacedqr_path}', 'rb'))
            page = qredit.getPage(0)
            newlabel.addPage(page)
            print("added to print")
            os.remove(lacedqr_path)
            os.remove(output)

            page = edit.getPage(1)
            page.cropBox.upperLeft = (30, 550)
            page.cropBox.lowerRight = (550, 240)
            page.mediaBox.upperLeft = (30, 550)
            page.mediaBox.lowerRight = (550, 240)
            page.bleedBox.upperLeft = (30, 550)
            page.bleedBox.lowerRight = (550, 240)
            page.artBox.upperLeft = (30, 550)
            page.artBox.lowerRight = (550, 240)
            page.trimBox.upperLeft = (30, 550)
            page.trimBox.lowerRight = (550, 240)
            newlabel.addPage(page)
        else:
            page = edit.getPage(0)
            page.cropBox.upperLeft = (60, 415)
            page.cropBox.lowerRight = (500, 180)
            page.mediaBox.upperLeft = (60, 415)
            page.mediaBox.lowerRight = (500, 180)
            page.bleedBox.upperLeft = (60, 415)
            page.bleedBox.lowerRight = (500, 180)
            page.artBox.upperLeft = (60, 415)
            page.artBox.lowerRight = (500, 180)
            page.trimBox.upperLeft = (60, 415)
            page.trimBox.lowerRight = (500, 180)
            newlabel.addPage(page)

            page = edit.getPage(1)
            page.cropBox.upperLeft = (185, 720)
            page.cropBox.lowerRight = (425, 300)
            page.mediaBox.upperLeft = (185, 720)
            page.mediaBox.lowerRight = (425, 300)
            page.bleedBox.upperLeft = (185, 720)
            page.bleedBox.lowerRight = (425, 300)
            page.artBox.upperLeft = (185, 720)
            page.artBox.lowerRight = (425, 300)
            page.trimBox.upperLeft = (185, 720)
            page.trimBox.lowerRight = (425, 300)
            page.rotate(90)
            aliasqr = PdfFileWriter()
            aliasqr.addPage(page)
            aliasqr_path = os.path.join(file_dir, 'aliasqr.pdf')
            Output = open(f'{aliasqr_path}', 'wb')
            aliasqr.write(Output)
            Output.close()
            
            # alias qr code to image
            doc = fz.open(aliasqr_path)
            page = doc.load_page(0)  # number of page
            pix = page.get_pixmap(dpi=300)
            output = os.path.join(file_dir, "outfile.png")
            pix.save(output)
            print("saved qr as image")

            # gamma increase
            im = Image.open(output).convert('L')
            imnp = np.array(im)/255
            gamma=0.2
            new = ((imnp**(1/gamma))*255).astype(np.uint8)
            Image.fromarray(new).save(output)
            print("gamma increased")

            # back to pdf
            doc = fz.open()
            img = fz.open(output)  # open pic as document
            rect = img[0].rect  # pic dimension
            pdfbytes = img.convert_to_pdf()  # make a PDF stream
            img.close()  # no longer needed
            imgPDF = fz.open("pdf", pdfbytes)  # open stream as PDF
            page = doc.new_page(width = rect.width, height = rect.height)  # pic dimension
            page.show_pdf_page(rect, imgPDF, 0)  # image fills the page
            doc.save(aliasqr_path)
            print("saved as new pdf")

            # add qr pdf to print
            qredit=PdfFileReader(open(f'{aliasqr_path}', 'rb'))
            page = qredit.getPage(0)
            newlabel.addPage(page)
            print("added to print")
            os.remove(aliasqr_path)
            os.remove(output)
            

    new_label_path = os.path.join(file_dir, 'newlabel.pdf')
    Output = open(f'{new_label_path}', 'wb')
    newlabel.write(Output)
    Output.close()
    messagebox.showinfo(title="Done", message="Labels ready to print!")
    print("done")


label1 = tk.Label(root, text='Add Laced and/or Alias labels here: ')
label1.grid(column=0,row=0, padx=5, pady =5)

button2 = tk.Button(text="Choose Files", command=file_chooser)
button2.grid(column=0,row=1, padx=5, pady=10)

button1 = tk.Button(text="Submit Labels", command=laced_label)
button1.grid(column=0,row=3, padx=5, pady =20)

root.mainloop()
