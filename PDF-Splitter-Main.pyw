from tkinter import *
from ttkwidgets.autocomplete import AutocompleteEntry
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkinter import ttk
from PIL import Image,ImageTk
from pdf2image import convert_from_path
from pikepdf import Pdf
import os
import os.path
from os.path import dirname
import easygui
import random
import time
from datetime import datetime
import logging

start_time = time.time()
now = datetime.now()
dt_string = now.strftime("%m-%d-%Y_%H-%M-%S")
preLogTxt = ''


def preLog(text):
    global preLogTxt
    preLogTxt = preLogTxt + '['+str(time.time())+']:  ' + text + '\n'
    
def checkLogFolder():
    preLog("Checking if log folder exists...")
    if not os.path.exists(os.getcwd()+'/logs'):
        preLog("Folder didnt exist, attempting to create a new log folder")
        folderLocation = os.getcwd()+'/logs'
        os.makedirs(folderLocation)
        preLog("Created a new log folder at "+folderLocation)
    else:
        preLog("Log Folder Exists")

def initLogging():
    logging.basicConfig(filename="logs/"+dt_string+'.txt', level=logging.INFO, format="%(asctime)s %(message)s")

def log(text):
    print('['+str(time.time())+']:  ' + text)
    logging.info('['+str(time.time())+']:  '+text)

log('Setting Project Paths....')
project_path = os.getcwd() + '\\'
log('+ project path set')
employee_path = dirname(os.getcwd()) + '\\'
log('+ employee path set')
library_path =os.getcwd()+'\\'+"poppler-22.04.0\\Library\\bin"
log('+ library path set')
file_names_path = project_path+"FileNames.txt"
log('+ file names path set')
log('Project Paths Set')

cutsIndex=0
previousIndex=0
files = []
Buttons = []
ButtonsWithCuts = []
Entries = []
photos = []

def setPathsWithGUI():
  log('Opening Auto Complete Text File...')
  global a_file
  a_file = open(file_names_path, "r")
  log('Auto Complete Text File Open')
  log('Reading Contents of the Auto Complete Text File...')
  file_contents = a_file.read()
  log('Auto Complete Text File Contents Read')

  log('Setting Autocomplete Values...')
  global autocompletevalues
  autocompletevalues = file_contents.splitlines()
  autocompletevalues.sort()
  log('Autocomplete Values Set')
  log('Closing Auto Complete Text File....')
  a_file.close()
  log('Auto Complete Text File Closed')

  log('Prompting User to Select the PDF File...')
  global pageDest
  pageDest = easygui.fileopenbox(msg=None, title="Please select the pdf file", default=employee_path+'\\*.pdf', filetypes = ["*.pdf"])
  if(pageDest is not None):
    log('PDF File Location Obtained')
  else:
    logging.exception("No PDF File Selected")


  msg = "Please select the folder to output to: "
  title = "Folder to output to..."

  log('Prompting User to Select the Output Folder Destination...')
  global outputDest
  outputDest = easygui.diropenbox(msg, title, default=employee_path + r"\\*")
  if(pageDest is not None):
    log('Output Folder Destination Obtained')
  else:
    logging.exception("No Output Folder Destination Selected")


def createWindow():
  log("Creating Root Window...")
  global root
  root = Tk()
  log("Setting Root Window Attributes")
  root.title('Employee File Master')
  root.geometry(f"1920x1080-1920+0")
  root.state('zoomed')
  log("Root Window Created")

def colorFrame():
  log("Starting Random Frame Color Creation")
  r = lambda: random.randint(10,150)
  r2 = lambda: random.randint(60,245)

  prerand = []

  match random.randint(0,2):
    case 0:
      prerand = [r2(),r(),r()]
    case 1:
      prerand = [r(),r2(),r()]
    case 2:
      prerand = [r(),r(),r2()]
    
  preshaderand = prerand.copy()

  indexRand = 0
  for x in preshaderand:
    preshaderand[indexRand] = preshaderand[indexRand]+10  
    indexRand = indexRand + 1

  global rand_color
  rand_color = '#%02X%02X%02X' % tuple(prerand)
  log("Random Color Created")
  global shaderand
  shaderand = '#%02X%02X%02X' % tuple(preshaderand)
  log("Shaded Random Color Created")


def createFrame():
  log("Creating Main Frame...")
  global main_frame
  main_frame = Frame(root, bg=rand_color)
  main_frame.pack(fill=BOTH,expand=1)
  log("Main Frame Created")


# Create A Canvas
def createCanvas():
  log("Creating the Canvas...")
  global my_canvas
  my_canvas = Canvas(main_frame, bg=rand_color)
  my_canvas.pack(side=LEFT,fill=BOTH,expand=1)

  log("Creating a Scrollbar...")
  y_scrollbar = ttk.Scrollbar(main_frame,orient=VERTICAL,command=my_canvas.yview)
  y_scrollbar.pack(side=RIGHT,fill=Y)
  log("Scrollbar Created")
  log("Binding the Scrollbar to the Canvas...")
  my_canvas.configure(yscrollcommand=y_scrollbar.set)
  my_canvas.bind("<Configure>",lambda e: my_canvas.config(scrollregion= my_canvas.bbox(ALL)))
  log("Scrollbar Bound to Canvas")
  log("Creating the Second Frame...")
  global second_frame
  second_frame = Frame(my_canvas, bg=shaderand)
  second_frame.grid_columnconfigure(1, minsize=60)  # Here
  log("Second Frame Created")
  log("Creating Canvas Window...")
  my_canvas.create_window((0,0),window= second_frame, anchor="nw")
  my_canvas.configure(yscrollincrement='103')
  log("Canvas Window Created")

  log("Binding the Mouse Wheel to the Scrollbar...")
  my_canvas.bind('<MouseWheel>', lambda event: my_canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
  second_frame.bind('<MouseWheel>', lambda event: my_canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

  root.bind('<Home>', lambda event: scrollDown(-1))
  root.bind('<End>', lambda event: scrollDown(1))

  log("Mouse Wheel Bound to Scrollbar")

  log("Creating Text Box Images from PDF Pages...")
  global pages
  pages = convert_from_path(pageDest,size=(600,776),poppler_path = library_path)
  # Empty list for storing images
  # Storing the converted images into list
  for i in range(len(pages)):
    photos.append(ImageTk.PhotoImage(pages[i]))
  # Adding all the images to the text widget
  log("Text Box Images Created")

def scrollDown(event):
  my_canvas.yview_scroll(int(event)*2, "units")

def addButtonEnabled(i):
  if i in ButtonsWithCuts:
      Buttons[i].configure(bg='#ecf0f1')          
      ButtonsWithCuts.remove(i)
      ButtonsWithCuts.sort()
  else: 
      Buttons[i].configure(bg='#3498db')          
      ButtonsWithCuts.append(i)
      ButtonsWithCuts.sort()

def addCut(i):
  global previousIndex
  log(str((previousIndex, i+1)))
  files.append((previousIndex, i+1))
  previousIndex = i+1

def finishCuts():
  log("Finishing Cuts...")
  ButtonsWithCuts.sort()
  for i in ButtonsWithCuts:
      addCut(i)

  addCut(len(pages))
  newindex=0
  for pageRange in files:
    pdf = Text(second_frame, bg="#2c3e50",width=75)
    pdf.grid(row = newindex*2, column = 2, sticky = "e")
    for page in range(pageRange[0],pageRange[1]):
        if page < len(pages):
          pdf.image_create(END,image=photos[page])
          pdf.insert(INSERT, "\n\n")
          pdf.config(state='disabled')
    E = AutocompleteCombobox(second_frame, completevalues=autocompletevalues)
    E.grid(row = newindex*2+1, column = 2, sticky = "ew")
    Entries.append(E)
    newindex=newindex+1
    
  B3 = Button(second_frame, text ="Make The Cuts")
  B3.configure(command=lambda: makeCuts())
  B3.grid(row = newindex*2, column = 2, sticky = "new")
  my_canvas.yview_moveto('0')

def CheckName(output_filename):
  if os.path.isfile(outputDest + '/' + output_filename + '.pdf'):
      ofilename = output_filename
      index3 = 2
      while os.path.isfile(outputDest + '/' + output_filename + '.pdf'):
        output_filename = ofilename + ' ' + str(index3)
        index3 = index3 + 1
  return output_filename

def makeCuts():
  log("Making the Cuts...")
  log(str(files))
  log("Opening the PDF")
  pdf = Pdf.open(pageDest)
  log("PDF Opened")
  new_pdf_files = [ Pdf.new() for i in files ]
  new_pdf_index = 0
  filename = "newFile"

  log("Opening Text Auto Complete File")
  a_file = open(file_names_path, "a")
  log("Text Auto Complete File Opened")
  
  log("Assigning Pages To Files...")
  for n, page in enumerate(pdf.pages):
    
      if n in list(range(*files[new_pdf_index])):
          # add the `n` page to the `new_pdf_index` file
          new_pdf_files[new_pdf_index].pages.append(page)
          log(f"Assigning Page {n} to the file {new_pdf_index}")
      else:
          # make a unique filename based on original file name plus the index
          name, ext = os.path.splitext(filename)
          #output_filename = f"{name}-{new_pdf_index}.pdf"
          output_filename = Entries[new_pdf_index].get().strip()
          # save the PDF file
          #new_pdf_files[new_pdf_index].save(output_filename)
          #new_pdf_files[new_pdf_index].save(outputDest + '/' + output_filename + '.pdf')
          log(f"File: {output_filename} saved.")
          # go to the next file
          new_pdf_index += 1
          # add the `n` page to the `new_pdf_index` file
          new_pdf_files[new_pdf_index].pages.append(page)
          log(f"Assigning Page {n} to the file {new_pdf_index}")

  log("Saving Files to Disk...")
  pdffileIndex = 0
  for pdffile in new_pdf_files:
    # save the last PDF file
    name, ext = os.path.splitext(filename)
    #output_filename = f"{name}-{new_pdf_index}.pdf"
    output_filename = Entries[pdffileIndex].get().strip()
    if (output_filename not in autocompletevalues) and (output_filename != '_') and (output_filename[-1] == '_'):
      a_file.write("\n")
      a_file.write(output_filename[:-1])

    if (output_filename[-1] == '_' and output_filename != '_'):
      output_filename = output_filename[:-1]
    
    if output_filename != '_':
      output_filename = CheckName(output_filename)
      pdffile.save(outputDest + '/' + output_filename + '.pdf')
      log(f"File: {output_filename} saved.")
    else:
      log(f"File: {output_filename} discarded.")
    pdffileIndex = pdffileIndex+1
  root.destroy()
  pdf.close()
  a_file.close()
  os.rename(pageDest, os.path.dirname(pageDest) + '\\' + CheckName("_Master Scanned File") + '.pdf')

def main():
  checkLogFolder()
  initLogging()

  log("Begin Log")
  log(preLogTxt)

  setPathsWithGUI()
  createWindow()
  colorFrame()
  createFrame()
  createCanvas()
  
  index = 0
  i=0
  for photo in photos:
      pdf = Text(second_frame, bg="grey", width=75)#,yscrollcommand=scrol_y.set,)
      pdf.grid(row = index, column = 0, sticky = "w")
      pdf.image_create(END,image=photo)
      pdf.config(state='disabled')
      if i != len(pages)-1:
        B = Button(second_frame, text ="Slice Page "+str(i+1), bg="#ecf0f1")
        B.configure(command=lambda i=i: addButtonEnabled(i))
        B.grid(row = index+1, column = 0, sticky = "ew")
        Buttons.append(B)
      i=i+1
      index=index+2

  B2 = Button(second_frame, text ="Finish")
  B2.configure(command=lambda: finishCuts())
  B2.grid(row = index, column = 0, sticky = "ew")
  Buttons.append(B2)
  Buttons.append(B2)

  # Ending of mainloop
  root.mainloop()

if __name__ == "__main__":
   try:
      main()
   except Exception as e:
      logging.exception("main crashed. Error: %s", e)
      print(e)

