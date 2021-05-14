import glob2
from pymongo import MongoClient

client = MongoClient(host="mongodb://quad-0.tepper.cmu.edu:32000/soco",retryWrites=False)
db = client.soco
data = []
for x in glob2.glob("2021*/final_images/*.jpeg"):
    filename = x.split("/")[-1]
    url = "https://convmind-images.s3.us-east-2.amazonaws.com/news/images/"+filename
    timestamp = filename.split("_")[1].replace(".jpeg","")
    data.append({"url":url, "filename":filename.split("_")[0]+".mp4", "timestamp":timestamp  })

db.video_demo.insert_many(data)
