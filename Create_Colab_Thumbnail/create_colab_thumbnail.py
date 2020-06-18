from PIL import Image, ImageFont, ImageDraw
import numpy as np
import cv2
import sys
import pyperclip
import argparse


SCRIPT_BASE_PATH = sys.path[0]
parser = argparse.ArgumentParser()
parser.add_argument('number', help='the problem number'.title(), type=int)

problem_number = str(parser.parse_args().number)
problem_number = '#' + problem_number.zfill(2)

video_description = '''{}.شرح جوجل كولاب | Google Colab :
السلام عليكم يا شباب فى الفيديو ده ان شاء الله هنشرح موضوع جديد فى جوجل كولاب :


يا رب الفيديو يعجبكم وماتنساش تعمل اشتراك  🔥🔥 
 و لايك 👍👍  و تفعل الجرس 🔔🔔
 عشان يوصلك كل جديد وشير الفيديو عشان المنفعة تعم 
=====================================================
🔶 الكورس كامل
================

https://www.youtube.com/playlist?list=PLO1D3YWS7ep0yi84ANyK4yJMDmMon_j5t
=====================================================
🔶 لو مش عارف يعنى ايه Jupyter او ازاى تستخدمه شوف الفيديو ده
=========================================================
https://www.youtube.com/watch?v=1Hn4wc_M3Ew
=====================================================
🔶 جوجل كولاب
===============
https://colab.research.google.com/
=====================================================
🔶 تواصل معى على:
==================
Linkedin:
https://www.linkedin.com/in/karim-elgazar
Facebook:
https://www.facebook.com/karimCodes
Twitter:
https://www.twitter.com/karimCodes
Github:
https://github.com/karimelgazar
===================================================
Google colabs,colabs,tensorflow colabs,what is colabs,get started with colabs,google colaboratory,coding tensorflow,machine learning tutorials,learn machine learning,ML,intro to google colabs,how to use colabs,Jupyter notebooks,jupyter,ML notebooks,run ml code,colab series,TensorFlow,Google CoLabs,TensorFlow developers,ai,google ai,شرح جوجل كولاب,شرح google colab,opencv,computer vision,كريم الجزار,كورسات,بايثون,python
===================================================
#karimCodes #كريم_الجزار #karim_elgazar
'''.format(
    # ! don't include the hashtag sign (#) for the description part
    problem_number[1:]
)


pyperclip.copy(video_description)
# نقص 300 من احداثى y المعطى فى gimp
coordination = (75,30)
color = (0, 166, 242)  # BGR
size = 300  # font size

thumbnail = cv2.imread(SCRIPT_BASE_PATH + "/colab.png")


# Make into PIL Image
im_p = Image.fromarray(thumbnail)

# Get a drawing context
draw = ImageDraw.Draw(im_p)
nirmala_bold = ImageFont.truetype(
    "/home/km/.local/share/fonts/nirmalab.ttf", size)
draw.text(coordination,
          problem_number,
          color,
          font=nirmala_bold)

# Convert back to OpenCV image and save
result_o = np.array(im_p)

# Save the Thumbnail
output_path = '/home/km/Videos/'
cv2.imwrite(output_path + problem_number + '.png', result_o)





















