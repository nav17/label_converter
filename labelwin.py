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
import shutil

# gen gui
root = tk.Tk()
root.title('Label Converter')

root.geometry("310x330")
root.eval('tk::PlaceWindow . center')
root.columnconfigure(0)

menu = tk.Menu(root)
root.config(menu=menu)
filemenu=tk.Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Exit", command=root.quit)

n_rows =5
n_columns =2
for i in range(n_rows):
    root.grid_rowconfigure(i,  weight =1)
for i in range(n_columns):
    root.grid_columnconfigure(i,  weight =1)

frame = tk.Frame(root)
frame.grid(column=0, row=2, padx=20, pady =15, columnspan=2)

lb = tk.Listbox(frame, width="27", height="10")
lb.grid(column=0,row=0)

class AutoScrollbar(tk.Scrollbar):
    def set(self, low, high):
        if float(low) <= 0.0 and float(high) >= 1.0:
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        tk.Scrollbar.set(self, low, high)

scrollbarY = AutoScrollbar(frame)
scrollbarY.config(command=lb.yview)
scrollbarY.grid(column=1,row=0, sticky="ns")
scrollbarX = AutoScrollbar(frame, orient="horizontal")
scrollbarX.config(command=lb.xview)
scrollbarX.grid(column=0,row=1, sticky="ew")
lb.config(yscrollcommand=scrollbarY.set, xscrollcommand=scrollbarX.set)

file_list = []

def file_chooser():
    files = fd.askopenfilenames(parent=root, title='Choose a File')
    for file in files:
        print("chosen: " + file)
        file_list.append(file)
        lb.insert("end", file)

def make_label():
    print(file_list)
    newlabel = PdfFileWriter()
    i = 0
    file_dir = os.path.dirname(file_list[0])
    temp_dir = os.path.join(file_dir, "temp")
    if os.path.isdir(temp_dir):
        shutil.rmtree(temp_dir)
    os.mkdir(temp_dir)
    for file in file_list:
        edit=PdfFileReader(open(f'{file}', 'rb'))
        print(file)
        file_dir = os.path.dirname(file)
        file_name = os.path.basename(file)
        print(file_name)
        i+=1
        if file_name.endswith('- Shipping Label.pdf'):
            # laced label
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
            lacedqr_path = os.path.join(temp_dir, 'lacedqr'+ str(i) +'.pdf')
            Output = open(f'{lacedqr_path}', 'wb')
            Output = open(f'{lacedqr_path}', 'wb')
            lacedqr.write(Output)
            Output.close()
            
            # qr code to image
            doc = fz.open(lacedqr_path)
            page = doc.load_page(0)
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
            img = fz.open(output)
            rect = img[0].rect
            pdfbytes = img.convert_to_pdf()
            img.close()
            imgPDF = fz.open("pdf", pdfbytes)
            page = doc.new_page(width = rect.width, height = rect.height)
            page.show_pdf_page(rect, imgPDF, 0) 
            doc.save(lacedqr_path)
            print("saved as new pdf")

            # add qr pdf to print
            qr_file = open(f'{lacedqr_path}', 'r+b')
            qredit=PdfFileReader(qr_file)
            page = qredit.getPage(0)
            newlabel.addPage(page)
            print("added to print")
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
            # alias label
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
            aliasqr_path = os.path.join(temp_dir, 'aliasqr' + str(i) + '.pdf')
            Output = open(f'{aliasqr_path}', 'wb')
            aliasqr.write(Output)
            Output.close()
            
            # alias qr code to image
            doc = fz.open(aliasqr_path)
            page = doc.load_page(0)
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
            img = fz.open(output)
            rect = img[0].rect
            pdfbytes = img.convert_to_pdf()
            img.close()
            imgPDF = fz.open("pdf", pdfbytes)
            page = doc.new_page(width = rect.width, height = rect.height)
            page.show_pdf_page(rect, imgPDF, 0)
            doc.save(aliasqr_path)
            print("saved as new pdf")

            # add qr pdf to print
            qr_file = open(f'{aliasqr_path}', 'r+b')
            qredit=PdfFileReader(qr_file)
            page = qredit.getPage(0)
            newlabel.addPage(page)
            print("added to print")
            os.remove(output)
            
    if file_list == []:
        messagebox.showwarning(message="No labels selected")
    
    new_label_path = os.path.join(file_dir, 'newlabel.pdf')
    Output = open(f'{new_label_path}', 'wb')
    newlabel.write(Output)
    Output.close()
    
    messagebox.showinfo(title="Done", message="Labels ready to print!")
    os.startfile(new_label_path)
    print("done")

def clear_list():
    file_list.clear()
    lb.delete(0,'end')

label1 = tk.Label(root, text='Add Laced and/or Alias labels here: ')
label1.grid(column=0,row=0, padx=5, pady =5, columnspan=2)

button2 = tk.Button(text="Choose Files", command=file_chooser)
button2.grid(column=0,row=1, padx=5, pady=0)

button1 = tk.Button(text="Submit Labels", command=laced_label)
button1.grid(column=0,row=3, pady =0, columnspan=2)

button3 = tk.Button(text="Clear", command=clear_list)
button3.grid(column=1,row=1, pady =0)

label2 = tk.Label(root)
label2.grid(column=0, row=4, columnspan=2)

root.mainloop()
