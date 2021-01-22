
import tkinter as tk
from tkinter import scrolledtext
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image
import sys
from utils import stegImage, genTextData, genImageData, saveFormat
from pyperclip import copy

class Window:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('855x500+250+100')
        self.root.title('StegMaker v2.0')
        self.root.configure(relief=tk.GROOVE)
        self.initializeFrames()

        
    def initializeFrames(self):

        self.mainFrame = tk.Frame(self.root)
        
        self.topFrame = tk.Frame(self.mainFrame)
        self.titleFrameTop = tk.Frame(self.topFrame, height=1, bg='gray50')

        self.textFrame = tk.Frame(self.topFrame)
        self.topText = tk.Label(self.textFrame, anchor=tk.W, justify=tk.LEFT, font=('Helvitica',10))
        self.topRightButton = tk.Button(self.textFrame, width=10, bg='gray90', relief=tk.GROOVE)
        self.radioButton1 = tk.Radiobutton(self.textFrame, font=('Helvitica', 10))
        self.radioButton2 = tk.Radiobutton(self.textFrame, font=('Helvitica', 10))
        self.radioButton3 = tk.Radiobutton(self.textFrame, font=('Helvitica', 10))
        
        self.scrolledText = scrolledtext.ScrolledText(self.topFrame, bg='gray90', relief=tk.GROOVE, height=15, width=25, wrap=tk.WORD)
        self.titleFrameBottom = tk.Frame(self.topFrame, height=1, bg='gray50')


        self.emptyFrame = tk.Frame(self.mainFrame)


        self.bottomFrame = tk.Frame(self.mainFrame)
        self.bottomMenuFrame = tk.Frame(self.bottomFrame, height=1, bg='gray50')
        self.bottomLeftButton = tk.Button(self.bottomFrame, text='Exit', width=8, bg='gray90', relief=tk.GROOVE, command=lambda:self.root.destroy())
        self.bottomRightButton1 = tk.Button(self.bottomFrame, width=8, bg='gray90', relief=tk.GROOVE)
        self.bottomRightButton2 = tk.Button(self.bottomFrame, width=8, bg='gray90', relief=tk.GROOVE)

        self.mainFrame.pack(fill=tk.BOTH, expand=tk.TRUE)

    
    def openImage(self):
        imageName = askopenfilename(filetypes=[('Image Files', ['*.jpeg', '*.jpg', '*.png'])])
        if imageName:
            self.imageFormat = imageName.split('.')[-1]
            if self.imageFormat in ['png', 'jpg', 'jpeg']:
                self.image = Image.open(imageName, 'r')
                self.bottomRightButton2.configure(state=tk.NORMAL)
            else:
                tk.messagebox.showwarning('warning', 'Unsupported file format\n\nSupported formats: [png, jpg, jpeg]')

    
    def saveAsImage(self, image, fileFormat):
        path = asksaveasfilename(filetypes=[('Image Files', fileFormat)], defaultextension=fileFormat[0])
        image.saveImage(path)
        self.root.destroy()


    def homePage(self):
        self.mainFrame.destroy()
        self.initializeFrames()

        self.topText.configure(text='Welcome to stegmaker!\n\nEncode: hide data inside a cover image\nDecode: extract data from a steg image', width=100)
        self.bottomRightButton1.configure(text='Encode', command=lambda:self.encodePage1())
        self.bottomRightButton2.configure(text='Decode', command=lambda:self.decodePage1(), state=tk.NORMAL)

        self.devMode = tk.IntVar(self.root, 0)
        self.developerMode = tk.Checkbutton(self.mainFrame, text='Developer Mode (more options for decoding)', width=100, anchor=tk.W, variable=self.devMode)
        
        self.topFrame.pack(fill=tk.X)
        self.titleFrameTop.pack(fill=tk.X, padx=10, pady=15)
        self.textFrame.pack(fill=tk.X)
        self.topText.pack(side=tk.LEFT, padx=15)
        self.titleFrameBottom.pack(fill=tk.X, padx=10, pady=15)

        self.emptyFrame.pack(fill=tk.BOTH, expand=tk.TRUE)

        self.developerMode.pack(fill=tk.X, padx=20, pady=10)

        self.bottomFrame.pack(fill=tk.X)
        self.bottomMenuFrame.pack(fill=tk.X, padx=10)
        self.bottomLeftButton.pack(side=tk.LEFT, padx=15, pady=15)
        self.bottomRightButton2.pack(side=tk.RIGHT, padx=15, pady=15)
        self.bottomRightButton1.pack(side=tk.RIGHT, pady=15)
    

    def encodePage1(self):
        self.mainFrame.destroy()
        self.initializeFrames()

        self.mode = tk.StringVar(self.root, 't')

        self.topText.configure(text='Choose a cover image\n\n\nChoose data type to encode', width=30)
        self.topRightButton.configure(text='Open File...', command=lambda:self.openImage())
        self.radioButton1.configure(text='text', variable=self.mode, value='t')
        self.radioButton2.configure(text='image', variable=self.mode, value='i')
        self.bottomRightButton1.configure(text='back', command=lambda:self.homePage())
        self.bottomRightButton2.configure(text='next', command=lambda:self.encodePage2(), state=tk.DISABLED)

        self.topFrame.pack(fill=tk.X)
        self.titleFrameTop.pack(fill=tk.X, padx=10, pady=15)
        self.textFrame.pack(fill=tk.X)
        self.topText.grid(column=0, row=0, columnspan=3, rowspan=4, sticky=tk.W, padx=15)
        self.topRightButton.grid(column=3, row=0, sticky=tk.W)
        self.radioButton1.grid(column=3, row=3, sticky=tk.SW)
        self.radioButton2.grid(column=4, row=3, sticky=tk.SW)
        self.titleFrameBottom.pack(fill=tk.X, padx=10, pady=15)

        self.emptyFrame.pack(fill=tk.BOTH, expand=tk.TRUE)
        
        self.bottomFrame.pack(fill=tk.X)
        self.bottomMenuFrame.pack(fill=tk.X, padx=10)
        self.bottomLeftButton.pack(side=tk.LEFT, padx=15, pady=15)
        self.bottomRightButton2.pack(side=tk.RIGHT, padx=15, pady=15)
        self.bottomRightButton1.pack(side=tk.RIGHT, pady=15)


    def encodePage2(self):
        self.mainFrame.destroy()
        self.initializeFrames()

        self.coverImage = stegImage(self.image.copy())
        self.coverFormat = self.imageFormat
        self.coverImage.encodeMode(self.mode.get())
        self.mode = self.mode.get()

        if self.mode == 't':
            self.encodePage2a()
        elif self.mode == 'i':
            self.encodePage2b()


    def encodePage2a(self):
        self.topText.configure(text='Type text that you want to encode:')
        self.bottomRightButton1.configure(text='back', command=lambda:self.encodePage1())
        self.bottomRightButton2.configure(text='next', command=lambda:self.encodePage3())

        self.topFrame.pack(fill=tk.X)
        self.titleFrameTop.pack(fill=tk.X, padx=10, pady=15)
        self.textFrame.pack(fill=tk.X)
        self.topText.pack(side=tk.LEFT, padx=15)
        self.scrolledText.pack(fill=tk.X, padx=15)
        self.titleFrameBottom.pack(fill=tk.X, padx=10, pady=15)

        self.emptyFrame.pack(fill=tk.BOTH, expand=tk.TRUE)

        self.bottomFrame.pack(fill=tk.X)
        self.bottomMenuFrame.pack(fill=tk.X, padx=10)
        self.bottomLeftButton.pack(side=tk.LEFT, padx=15, pady=15)
        self.bottomRightButton2.pack(side=tk.RIGHT, padx=15, pady=15)
        self.bottomRightButton1.pack(side=tk.RIGHT, pady=15)


    def encodePage2b(self):
        self.topText.configure(text='Choose image to encode inside cover image')
        self.bottomRightButton1.configure(text='back', command=lambda:self.encodePage1())
        self.bottomRightButton2.configure(text='next', command=lambda:self.encodePage3(), state=tk.DISABLED)
        self.topRightButton.configure(text='Open File...', command=lambda:self.openImage())

        self.topFrame.pack(fill=tk.X)
        self.titleFrameTop.pack(fill=tk.X, padx=10, pady=15)
        self.textFrame.pack(fill=tk.X)
        self.topText.pack(side=tk.LEFT, padx=15)
        self.topRightButton.pack(side=tk.LEFT, padx=90)
        self.titleFrameBottom.pack(fill=tk.X, padx=10, pady=15)

        self.emptyFrame.pack(fill=tk.BOTH, expand=tk.TRUE)
        
        self.bottomFrame.pack(fill=tk.X)
        self.bottomMenuFrame.pack(fill=tk.X, padx=10)
        self.bottomLeftButton.pack(side=tk.LEFT, padx=15, pady=15)
        self.bottomRightButton2.pack(side=tk.RIGHT, padx=15, pady=15)
        self.bottomRightButton1.pack(side=tk.RIGHT, pady=15)


    def encodePage3(self):
        if self.mode == 't':
            self.coverImage.encodeData(genTextData(self.scrolledText.get('1.0', 'end-1c')))
        elif self.mode == 'i':
            hiddenImage = self.image
            hiddenFormat = self.imageFormat
            self.coverImage.encodeSize(hiddenImage.size)
            self.coverImage.encodeFormat(hiddenFormat)
            self.coverImage.encodeData(genImageData(hiddenImage))
        self.coverImage.buildStegImage()

        self.mainFrame.destroy()
        self.initializeFrames()

        self.topText.configure(text='Steg Image created successfully!')
        self.bottomRightButton2.configure(text='Save File', command=lambda:self.saveAsImage(self.coverImage, ['*.png']))

        self.topFrame.pack(fill=tk.X)
        self.titleFrameTop.pack(fill=tk.X, padx=10, pady=15)
        self.textFrame.pack(fill=tk.X)
        self.topText.pack(side=tk.LEFT, padx=15)
        self.titleFrameBottom.pack(fill=tk.X, padx=10, pady=15)

        self.emptyFrame.pack(fill=tk.BOTH, expand=tk.TRUE)

        self.bottomFrame.pack(fill=tk.X)
        self.bottomMenuFrame.pack(fill=tk.X, padx=10)
        self.bottomLeftButton.pack(side=tk.LEFT, padx=15, pady=15)
        self.bottomRightButton2.pack(side=tk.RIGHT, padx=15, pady=15)

    
    def decodePage1(self):
        self.mainFrame.destroy()
        self.initializeFrames()

        self.mode = tk.IntVar(self.root, 1)

        self.topText.configure(text='Choose image to decode data from')
        self.topRightButton.configure(text='Open File...', command=lambda:self.openImage())
        self.radioButton1.configure(text='Automatic Decode', variable=self.mode, value=1)
        self.radioButton2.configure(text='Integer Decode', variable=self.mode, value=2)
        self.radioButton3.configure(text='Character Decode', variable=self.mode, value=3)
        self.bottomRightButton1.configure(text='back', command=lambda:self.homePage())
        self.bottomRightButton2.configure(text='next', command=lambda:self.decodePage2(), state=tk.DISABLED)

        self.topFrame.pack(fill=tk.X)
        self.titleFrameTop.pack(fill=tk.X, padx=10, pady=15)
        self.textFrame.pack(fill=tk.X)
        self.topText.grid(column=0, row=0, padx=15, sticky=tk.W)
        self.topRightButton.grid(column=1, row=0, padx=90)
        if self.devMode.get():
            tk.Frame(self.textFrame, height=30).grid(column=0, row=1)
            self.radioButton1.grid(column=0, row=2, padx=20, sticky=tk.W)
            self.radioButton2.grid(column=0, row=3, padx=20, sticky=tk.W)
            self.radioButton3.grid(column=0, row=4, padx=20, sticky=tk.W)
        self.titleFrameBottom.pack(fill=tk.X, padx=10, pady=15)

        self.emptyFrame.pack(fill=tk.BOTH, expand=tk.TRUE)
        
        self.bottomFrame.pack(fill=tk.X)
        self.bottomMenuFrame.pack(fill=tk.X, padx=10)
        self.bottomLeftButton.pack(side=tk.LEFT, padx=15, pady=15)
        self.bottomRightButton2.pack(side=tk.RIGHT, padx=15, pady=15)
        self.bottomRightButton1.pack(side=tk.RIGHT, pady=15)


    def decodePage2(self):
        self.mainFrame.destroy()
        self.initializeFrames()

        self.mode = self.mode.get()
        self.image = stegImage(self.image)

        if self.mode != 1 or self.image.decodeMode() == 't':
            self.decodePage2a()
        else:
            self.decodePage2b()


    def decodePage2a(self):
        if self.mode == 1:
            text = self.image.decodeText()
            self.topText.configure(text='Text extracted:')
       
        elif self.mode == 2:
            text = self.image.developerDecode('int')
            self.topText.configure(text='Data extracted (integers):')
        
        elif self.mode == 2:
            text = self.image.developerDecode('char')
            self.topText.configure(text='Data extracted (ASCII Characters):')

        self.bottomRightButton2.configure(text='copy text', command=lambda:copy(text))
        self.scrolledText.insert(tk.INSERT, text)
        self.scrolledText.configure(state=tk.DISABLED)

        self.topFrame.pack(fill=tk.X)
        self.titleFrameTop.pack(fill=tk.X, padx=10, pady=15)
        self.textFrame.pack(fill=tk.X)
        self.topText.pack(side=tk.LEFT, padx=15)
        self.scrolledText.pack(fill=tk.X, padx=15)
        self.titleFrameBottom.pack(fill=tk.X, padx=10, pady=15)

        self.emptyFrame.pack(fill=tk.BOTH, expand=tk.TRUE)

        self.bottomFrame.pack(fill=tk.X)
        self.bottomMenuFrame.pack(fill=tk.X, padx=10)
        self.bottomLeftButton.pack(side=tk.LEFT, padx=15, pady=15)
        self.bottomRightButton2.pack(side=tk.RIGHT, padx=15, pady=15)

    
    def decodePage2b(self):
        self.image.decodeSize()
        hiddenFormat = self.image.decodeFormat()
        hiddenImage = self.image.decodeImage()

        self.topText.configure(text='Image found!')
        self.bottomRightButton1.configure(text='preview', command=lambda:hiddenImage.show())
        self.bottomRightButton2.configure(text='save', command=lambda:self.saveAsImage(stegImage(hiddenImage), hiddenFormat))

        self.topFrame.pack(fill=tk.X)
        self.titleFrameTop.pack(fill=tk.X, padx=10, pady=15)
        self.textFrame.pack(fill=tk.X)
        self.topText.pack(side=tk.LEFT, padx=15)
        self.titleFrameBottom.pack(fill=tk.X, padx=10, pady=15)

        self.emptyFrame.pack(fill=tk.BOTH, expand=tk.TRUE)

        self.bottomFrame.pack(fill=tk.X)
        self.bottomMenuFrame.pack(fill=tk.X, padx=10)
        self.bottomLeftButton.pack(side=tk.LEFT, padx=15, pady=15)
        self.bottomRightButton2.pack(side=tk.RIGHT, padx=15, pady=15)
        self.bottomRightButton1.pack(side=tk.RIGHT, pady=15)


def main():
    window = Window()
    window.homePage()
    tk.mainloop()