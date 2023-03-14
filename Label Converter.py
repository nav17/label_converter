# v0.2
from PyPDF2 import PdfFileReader, PdfFileWriter
import os.path
import tkinter as tk
import os
import tkinter.filedialog as fd
import fitz as fz #pymupdf
import numpy as np
from tkinter import messagebox
from PIL import Image
import subprocess
import platform
import datetime

root = tk.Tk()
root.title('Label Converter')

if(platform.system() == "Darwin"):
    root.geometry("375x345")
elif(platform.system() == "Windows"):
    root.geometry("360x340")

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
frame.grid(column=0, row=3, padx=20, pady =10, columnspan=2)

if(platform.system() == "Darwin"):
    lb = tk.Listbox(frame, width="35", height="10")
elif(platform.system() == "Windows"):
    lb = tk.Listbox(frame, width="50", height="10")
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
        f = os.path.basename(file)
        lb.insert("end", f)
    if(file_list!=[]):
        button3.grid(column=0,row=2, padx=25, pady =0, sticky="W")

class label:
    def crop(page ,x1, y1, x2, y2):
        page.cropBox.upperLeft = (x1, y1)
        page.cropBox.lowerRight = (x2,y2)
        page.mediaBox.upperLeft = (x1, y1)
        page.mediaBox.lowerRight = (x2,y2)
        page.bleedBox.upperLeft = (x1, y1)
        page.bleedBox.lowerRight = (x2,y2)
        page.artBox.upperLeft = (x1, y1)
        page.artBox.lowerRight = (x2,y2)
        page.trimBox.upperLeft = (x1, y1)
        page.trimBox.lowerRight = (x2,y2)
    
    def load(self, page, file_dir):
        qr = PdfFileWriter()
        qr.addPage(page)
        qr_path = os.path.join(file_dir, 'qr.pdf')
        Output = open(f'{qr_path}', 'wb')
        qr.write(Output)
        Output.close()
        return qr_path

    def qr_to_image(self, qr_path, file_dir):
        doc = fz.open(qr_path)
        page = doc.load_page(0)
        pix = page.get_pixmap(dpi=300)
        output = os.path.join(file_dir, "outfile.png")
        pix.save(output)
        print("saved qr as image")
        return output

    def darken(self, output):
        im = Image.open(output).convert('L')
        imnp = np.array(im)/255
        gamma=0.2
        new = ((imnp**(1/gamma))*255).astype(np.uint8)
        Image.fromarray(new).save(output)
        print("gamma increased")
        return output

    def img_to_pdf(self, output, qr_path):
        doc = fz.open()
        img = fz.open(output)
        rect = img[0].rect
        pdfbytes = img.convert_to_pdf()
        img.close()
        imgPDF = fz.open("pdf", pdfbytes)
        page = doc.new_page(width = rect.width, height = rect.height)
        page.show_pdf_page(rect, imgPDF, 0)
        doc.save(qr_path)
        print("saved as new pdf")
        return qr_path
        
    def load_qr(self, qr_path, output, newlabel):
        qr_file = open(f'{qr_path}', 'rb')
        qr_edit = PdfFileReader(qr_file)
        page = qr_edit.getPage(0)
        newlabel.addPage(page)
        print("added to print")
        os.remove(output)
    
    def process(self, page, file_dir, newlabel):
        qr_path = self.load(page, file_dir)
        output = self.qr_to_image(qr_path, file_dir)
        output = self.darken(output)
        qr_path = self.img_to_pdf(output, qr_path)
        self.load_qr(qr_path, output, newlabel)
    
def make_label():
    newlabel = PdfFileWriter()
    if file_list == []:
        messagebox.showwarning(message="No labels selected")
    for file in file_list:
        infile = open(f'{file}', 'rb')
        edit=PdfFileReader(infile)
        print(file)
        file_dir = os.path.dirname(file)
        file_name = os.path.basename(file)
        page = edit.getPage(0)
        text = page.extract_text()

        # laced label
        if file_name.endswith('- Shipping Label.pdf') or text.startswith("INCLUDE"):
            page = edit.getPage(0)
            label.crop(page, 100, 710, 500, 475)
            label().process(page, file_dir, newlabel)

            page = edit.getPage(1)
            label.crop(page, 30, 560, 550, 250)
            newlabel.addPage(page)
        
        # kick game label
        elif text.endswith("item."):
            page = edit.getPage(0)
            label.crop(page, 110, 680, 485, 120)
            page.rotate(90)
            newlabel.addPage(page)

            page = edit.getPage(1)
            label.crop(page, 60,415, 500, 180)
            newlabel.addPage(page)
        
        # stockx label
        elif file_name.startswith('StockX'):
            page = edit.getPage(0)
            label.crop(page,25 ,860 , 570, 550)
            newlabel.addPage(page)

            page = edit.getPage(1)
            label.crop(page, 20, 565, 500, 240)
            newlabel.addPage(page)
        
        # alias label
        else:
            # dpd label
            if text.startswith("DPD"):
                label.crop(page, 60, 415, 500, 180)
                newlabel.addPage(page)
            #ups label
            else:
                page.rotate(90)
                newlabel.addPage(page)
            
            page = edit.getPage(1)
            label.crop(page, 185, 720, 425, 300)
            page.rotate(90)
            label().process(page, file_dir, newlabel)
    
        new_label_path = os.path.join(file_dir, 'Label Print '+ datetime.datetime.now().strftime('%Y-%m-%d')+'.pdf')
        new_label_path = os.path.normpath(new_label_path)
        Output = open(f'{new_label_path}', 'wb')
        newlabel.write(Output)
        qr_path = os.path.join(file_dir, 'qr.pdf')
        try:
            os.remove(qr_path)
        except:
            pass
        
    Output.close()
    if(switch.get() == 1):
        for file in file_list:
            os.remove(file)
        file_list.clear()
        lb.delete(0,'end')
    messagebox.showinfo(title="Done", message="Labels ready to print!")
    if(platform.system() == "Darwin"):
        subprocess.run(['open', new_label_path], check=True)
    elif(platform.system() == "Windows"):
        os.startfile(new_label_path)
    print("done")

def clear_list():
    file_list.clear()
    lb.delete(0,'end')
    button3.grid_forget()

switch = tk.IntVar()

label1 = tk.Label(root, text='Add labels here:')
label1.grid(column=0,row=0, padx=25, pady =5, columnspan=2, sticky="W")

button2 = tk.Button(text="Choose Files", command=file_chooser)
button2.grid(column=0,row=1, padx=25, pady=0, sticky="W")

button1 = tk.Button(text="Submit Labels", command=make_label)
button1.grid(column=0,row=4, pady =0, columnspan=2)

button3 = tk.Button(text="Clear List", command=clear_list)
button3.grid(column=1,row=2, padx=25, pady =0, sticky="E")

checkbox1 = tk.Checkbutton(root, text="auto-delete labels", variable=switch, onvalue=1, offvalue=0)
checkbox1.grid(column=1, row=1, padx=25, pady =0, sticky="E")

if(file_list == []):
    button3.grid_forget()
    checkbox1.grid(column=1, row=1, padx=25, pady =0, sticky="E")

label2 = tk.Label(root)
label2.grid(column=0, row=5, columnspan=2)

root.mainloop()