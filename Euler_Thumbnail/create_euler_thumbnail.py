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

video_description = '''مشروع أويلر مسألة Project Euler Problem {} | | {} 
السلام عليكم يا شباب فى الفيديو ده ان شاء الله هنحل مسالة رقم {} من مشروع أويلر

يا رب الفيديو يعجبكم وماتنساش تعمل اشتراك  🔥🔥 
 و لايك 👍👍  و تفعل الجرس 🔔🔔
 عشان يوصلك كل جديد وشير الفيديو عشان المنفعة تعم 
=====================================================
لو مش عارف يعنى ايه Jupyter او ازاى تستخدمه شوف الفيديو ده
===============================
https://www.youtube.com/watch?v=1Hn4wc_M3Ew
=====================================================
كل المسائل المحلولة
=================
https://www.youtube.com/playlist?list=PLO1D3YWS7ep3Zrh8B4SrhIsyxneg23x29
=====================================================
الحلول على Github
=================
https://github.com/karimelgazar/Project-Euler
=====================================================
Please Support Me On:
Linkedin:
https://www.linkedin.com/in/karim-elgazar
Facebook:
https://www.facebook.com/karimCodes
Twitter:
https://www.twitter.com/karimCodes
Github:
https://github.com/karimelgazar
===================================================
#karimCodes,arabic,عربي,introduction,Python (Programming Language),Tutorial (Media Genre),متطابقة أويلر,متطابقة اويلر,math pi hanan,mathpihanan,اويلر,وش سر جمال متطابقة اويلر,project euler,مشروع اويلر,حل مسألة,problem,project euler problem,أويلر,رياضيات,حساب,maths
===================================================
#karimCodes #LearnWithKarim #KarimElgazar'''.format(
    problem_number,
    problem_number,
    # ! don't include the hashtag sign (#) for the description part
    problem_number[1:]
)


pyperclip.copy(video_description)

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
