import sys
sys.path.insert(0, "/data/notebooks/")

import cv2
import os
from flir_image_extractor import flir_image_extractor
from PIL import Image
import numpy as np
global fir
fir = flir_image_extractor.FlirImageExtractor()


import subprocess
import json
import re
import base64

def read_image(filename, save_path, image):
    "Output: filename, save_path, image, thermal_image"
    # decode and save image
    #decoded = base64.b64decode(image)
    os.makedirs(os.path.dirname(save_path+filename), exist_ok=True)
    newFile = open(save_path+filename, "wb")
    newFile.write(image)
    newFile.close()
    # extract thermal_image
    thermal_image = read_thermal_image(save_path+filename)
    thermal_image = thermal_image.tobytes()
    return filename, save_path, image, thermal_image
    
def read_thermal_image(image_path):
    fir.process_image(image_path)
    ret, thermal_image = cv2.imencode('.PNG', fir.thermal_image_np.astype(np.uint8))
    return thermal_image
