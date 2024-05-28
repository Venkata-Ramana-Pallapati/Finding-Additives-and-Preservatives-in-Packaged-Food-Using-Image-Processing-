from  flask import Flask, render_template, request
import os, io
from google.cloud import vision
import pandas as pd
import re
import sys
import cv2
from werkzeug.utils import secure_filename
import smtplib
from smtplib import SMTP
from email.message import EmailMessage


app = Flask(__name__)
upload_folder = os.path.join('static', 'uploads')

app.config['UPLOAD'] = upload_folder

@app.route('/')
def index():
 return render_template("index.html")

@app.route('/', methods = ['POST'])




def getvalue():
 name = request.form['sname']
 if name:
  z=[name]
  arr = search(z)

  return render_template("index.html", arr=arr, l=len(arr))
 else:
  file = request.files['file']
  filename = secure_filename(file.filename)
  file.save(os.path.join(app.config['UPLOAD'], filename))
  img = os.path.join(app.config['UPLOAD'], filename)
  im = cv2.imread(img)
  z=google(file.filename)
  arr=search(z)
  return render_template("index.html", arr=arr, l=len(arr),img=img)

def search(z):
 #print(z)
 #df = pd.read_excel('C:\\Users\\sekha\\Downloads\\Dataset.xlsx')
 df =pd.read_excel('C:\\Users\\91939\\Downloads\\Dataset.xlsx')
 #df=pd.read_excel('Dataset.xlsx')
 ans=[]
 Data = {}
 for i, r in df.iterrows():
  Data[r[0]] = [r[1], r[2]]
 k=1
 #print(Data)

 for e in z:
  if e in Data:
   #print(e)
   ans.append([k,e,Data[e][0],Data[e][1]])
   k+=1
 #print(ans)

 return ans


def google(File_Name):
 #os.environ['GOOGLE_APPLICATION_CREDENTIALS'] =r"C:\Users\91939\PycharmProjects\pythonProject\venv\projectkey.json"
 os.environ['GOOGLE_APPLICATION_CREDENTIALS'] =r"C:\Users\91939\PycharmProjects\pythonProject\venv\ramu.json"




 # create client instance
 client = vision.ImageAnnotatorClient()
 #Folder_Path = r"C:\Users\sekha\PycharmProjects\pythonProject\static\uploads"
 Folder_Path = r"C:\Users\91939\PycharmProjects\pythonProject\static\uploads"

 with io.open(os.path.join(Folder_Path, File_Name), 'rb') as image_file:
  content = image_file.read()
 image = vision.Image(content=content)
 response =  client.text_detection(image=image)
 texts = response.text_annotations
 ans = ""
 for page in response.full_text_annotation.pages:
  for block in page.blocks:
   for paragraph in block.paragraphs:
    s = ""
    for word in paragraph.words:
     word_text = ''.join([symbol.text for symbol in word.symbols])
     s += word_text

    ans = ans + " " + s
   print(ans)



 # using regex module to filter the raw string
   ad = re.findall(r"\bINS\w+", ans)
   ad += re.findall(r"\bE\w+", ans)


 #print(ans)
 print(ad)
 ram=ans
 thanu=ram.split()
 for i in thanu:

  return ad
 print(ad)


if __name__ == "__main__":
 app.run(debug=True)
