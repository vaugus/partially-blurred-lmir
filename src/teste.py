import numpy as np
import scipy.ndimage
from tools import Tools

img = scipy.ndimage.imread('../input/images/colored/normal_focus/normal_focus_10.jpg', mode='L')

tools = Tools()
tools.save_image(img)