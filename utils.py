
from PIL import Image
from PIL.Image import Image as img


# Converts the Data string to hide to binary 
def genTextData(text):
    return [format(ord(i), '08b') for i in text]


# Creats a list of lists with the binary RGB values for pixels in an image 
def genImageData(image):
    imageData = image.getdata()
    result = []
    for i in range(len(image.getdata())):
        result += [format(value, '08b') for value in imageData[i][:3]]
    return result


# Creates a format() argument to use when generating binary data
def formatArg(data):
    value = 1
    while True:
        if data < 255**value:
            break
        value += 1
    return '0' + str(8 * value) + 'b'


# Splits a binary string into bytes and returns them in a list
def formatBin(binString):
    binList = []
    for i in range(0, len(binString), 8):
        binList.append(binString[i:i+8])
    return binList

# returns the format of an image in a form that can be used by the "asksaveasfilename" tkinter function
def saveFormat(imageFormat):
    if imageFormat == 'png':
        return ['*.png']
    elif imageFormat in ['jpg', 'jpeg']:
        return ['*.jpg', '*.jpeg']


# Image class and methods for encoding and decoding
# Takes an "opened" PIL Image object as an argument
class stegImage(img):
    def __init__(self, image):
        img.__init__(self)
        self.image = image.convert('RGBA')
        self.pixels = image.getdata()
        self.newPixels = []     # List for the modified pixels, used in encoding
        self.pixelCounter = 0   # Counter used for encoding and decoding


    # Modifies pixels to hide data, called by all encoding methods
    # Data must be entered in a list
    def modPix(self, data):
        result = []
        for i in range(len(data)):

            # Extracts three pixels at a time
            pixToChange = [value for value in self.pixels[self.pixelCounter][:3] +
                                              self.pixels[self.pixelCounter + 1][:3] +
                                              self.pixels[self.pixelCounter + 2][:3]]

            # Changes pixels to hide data
            for j in range(8):
                if data[i][j] == '0' and (pixToChange[j] % 2 != 0): 
                    pixToChange[j] -= 1
                elif data[i][j] == '1' and (pixToChange[j] % 2 == 0): 
                    if pixToChange[j] != 0:    
                        pixToChange[j] -= 1
                    else:
                        pixToChange[j] += 1
            
            # Change the last bit in the 3 pixels
            # makes it even (0) if there is more data to add or odd (1) if there is no more data
            if i == (len(data) - 1) and pixToChange[8] % 2 == 0:
                pixToChange[8] -= 1
            elif i != (len(data) - 1) and pixToChange[8] % 2 != 0:
                if pixToChange[8] != 0:
                    pixToChange[8] -= 1
                else:
                    pixToChange[8] += 1

            # Adds pixels to a list
            result += [tuple(pixToChange[0:3]), tuple(pixToChange[3:6]), tuple(pixToChange[6:9])]
            self.pixelCounter += 3
        
        self.newPixels += result
    

    # Encodes the encoding mode used in the steg image, either "t" for text or "i" for image
    def encodeMode(self, mode):
        self.modPix([format(ord(mode), '08b')])
    
    # Encodes the size of an image in the case of encoding an image
    def encodeSize(self, size):
        widthstr = format(size[0], formatArg(size[0]))
        heightstr = format(size[1], formatArg(size[1]))
        
        width = formatBin(widthstr)
        height = formatBin(heightstr)

        self.modPix(width)
        self.modPix(height)

    # Encode the format of the hidden image
    def encodeFormat(self, fileFormat):
        if fileFormat == 'png':
            hiddenFormat = 'p'
        elif fileFormat in ['jpg', 'jpeg']:
            hiddenFormat = 'j'
        self.modPix([format(ord(hiddenFormat), '08b')])
    
    # Encodes the main data, whether text or image data
    # Must be used after the "encodeMode", "encodeSize"(if needed) and "encodeFormat"(if needed) methods
    def encodeData(self, data):
        self.modPix(data)

    # Creates the final image containing the hidden data
    def buildStegImage(self):
        width = self.image.size[0]
        x = y = 0   # location variables for the pointer
        
        # builds the image pixel by pixel
        for pixel in self.newPixels:
            self.image.putpixel((x, y), pixel)
            
            # Moves the pointer
            if x < width - 1:
                x += 1
            else:
                x = 0
                y += 1
    

    # Extracts hidden data from an image, used by all decoding methods
    def extarctData(self):
        dataList = []
        while True:     
            byte = ''

            # Checks three pixles at a time
            pixelGroup = [value for value in self.pixels[self.pixelCounter][:3] +
                                             self.pixels[self.pixelCounter + 1][:3] +
                                             self.pixels[self.pixelCounter + 2][:3]]
            for i in range(8):
                if pixelGroup[i] % 2 == 0:
                    byte += '0'
                else:
                    byte += '1'
            
            dataList.append(byte)

            self.pixelCounter += 3   # increments counter by 3 (three pixels are checked at a time) 
            
            if pixelGroup[8] % 2 == 1:  # returns a chunk of data when the last bit in a pixel group is odd
                return dataList
    
    
    # Returns the mode used in encoding, "t" for text or "i" for image
    def decodeMode(self):
        return chr(int(''.join(self.extarctData()), 2))
    
    # returns the size of the hidden image
    def decodeSize(self):
        width = int(''.join(self.extarctData()), 2)
        height = int(''.join(self.extarctData()), 2)
        self.hiddenSize = tuple((width, height))

    # extracts the format of the hidden image, "p" for png or "j" for jpeg or jpg
    # returns the format in a form that can be used by the "asksaveasfilename" tkinter function
    def decodeFormat(self):
        hiddenFormat = chr(int(''.join(self.extarctData()), 2))

        if hiddenFormat == 'p':
            return ['*.png']
        elif hiddenFormat == 'j':
            return ['*.jpg', '*.jpeg']
    
    # Extracts text from the steg image and returns it as a string
    # Must be used after the "decodeMode" method 
    def decodeText(self):
        binaryList = self.extarctData()
        text = ''     # The final string of text 
        
        for byte in binaryList:
            text += chr(int(byte, 2))   # converts the byte into an ASCII character
        return text
    
    # Extracts the hidden image from a steg image as pixles and rebuilds it as a PIL Image object
    # Must be used after the "decodeMode" method
    def decodeImage(self):
        binaryList = self.extarctData()
        hiddenImage = Image.new(mode = 'RGB', size = self.hiddenSize)
        x = y = 0   # location variables for the pointer
        pixelList = []

        # Returns a list of tuples for each pixel
        for i in range(0, len(binaryList), 3):
            pixelList.append((int(binaryList[i], 2),
                               int(binaryList[i+1], 2),
                               int(binaryList[i+2], 2)))
        
        # Building the hidden image pixel by pixel
        for pixel in pixelList:
            hiddenImage.putpixel((x, y), pixel)
            
            # Moves the pointer
            if x < self.hiddenSize[0] - 1:
                x += 1
            else:
                x = 0
                y += 1
        return hiddenImage

    # uses the "extractData" method on the WHOLE steg image and returns a string of either the integer or ASCII values of the data extracted
    def developerDecode(self, mode):
        binaryList = []
        result = []
        
        # extracts EVERYTHING
        while self.pixelCounter < (self.image.size[0] * self.image.size[1]):
            binaryList.append(self.extarctData())

        # converts data into integers
        if mode == 'int':    
            for byte in binaryList:
                result.append(int(byte, 2))
            return ''.join(binaryList)
        
        # converts data into ASCII characters
        elif mode == 'char':
            for byte in binaryList:
                result.append(chr(int(byte, 2)))
            return ' '.join(binaryList)
        

    # restes the "pixelCounter" if you intentionally mess with it
    def resetPixelCounter(self):
        self.pixelCounter = 0
            
    # saves the steg image to a specfic path
    def saveImage(self, path):
        self.image.save(path)