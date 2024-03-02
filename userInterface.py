# Import the Tkinter and Pillow modules
from tkinter import *
from PIL import ImageTk, Image
import time



# Create a root window
root = Tk()

# Create a canvas widget
canvas = Canvas(root, width=1520, height=680, bg="black")


# Load an image file
img = Image.open("microphonePhoto.jpg")

# Resize the image if needed
img = img.resize((256, 256))

# Create an image object compatible with Tkinter
img = ImageTk.PhotoImage(img)
canvas.pack()

# Display the image object on the canvas
canvasImg = canvas.create_image(700, 300, image=img)

# Start the main loop
def startLoop():
    root.mainloop()
    
def moveImage(frequencyVal, noteFreq):
    # Move the image
    if (frequencyVal < noteFreq):
        canvas.move(canvasImg, 0, -10)
        canvas.update()
    elif (frequencyVal > noteFreq):
        canvas.move(canvasImg, 0, +10)
        canvas.update()

canvas.update()