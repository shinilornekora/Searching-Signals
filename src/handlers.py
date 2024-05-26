from src.io.utils import openFileExplorerAndReturnFileName
from src.convert.utils import convert2Png
from src.state.images_state import add_images, clear_images

import os

def exportHandler():
    print('I will handle exports')

storage = os.path.join(os.path.dirname(__file__), '..', 'temp', 'images') 

def importHandler():
    path = openFileExplorerAndReturnFileName()
    clear_images()
    images = convert2Png(path, storage)
    add_images(images)

def selectHandler(): 
    print('I will handle blueprint type selection')