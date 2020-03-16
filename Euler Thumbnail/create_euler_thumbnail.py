from PIL import Image, ImageFont, ImageDraw
import numpy as np
import cv2
import webbrowser
import sys
import pyperclip
import argparse


SCRIPT_BASE_PATH = sys.path[0]
parser = argparse.ArgumentParser()
parser.add_argument('number', help='the problem number'.title(), type=int)

problem_number = str(parser.parse_args().number)
problem_number = '#' + problem_number.zfill(3)

video_name = "مشروع أويلر مسألة Project Euler Problem {} || {} ".format(
    problem_number,
    problem_number)


pyperclip.copy(video_name)

coordination = (600, 650)
color = (67, 195, 244)  # BGR
size = 300  # font size

thumbnail = cv2.imread(SCRIPT_BASE_PATH + "/euler.png")


# Make into PIL Image
im_p = Image.fromarray(thumbnail)

# Get a drawing context
draw = ImageDraw.Draw(im_p)
nirmala_bold = ImageFont.truetype(
    "C:/Windows/Fonts/Nirmala UI/NirmalaB.ttf", size)
draw.text(coordination,
          problem_number,
          color,
          font=nirmala_bold)

# Convert back to OpenCV image and save
result_o = np.array(im_p)

# Save the Thumbnail
output_path = 'E:/Captures/'
cv2.imwrite(output_path + problem_number + '.png', result_o)
webbrowser.open(output_path)
