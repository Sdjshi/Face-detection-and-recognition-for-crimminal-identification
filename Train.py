#Training and creating classifier
import numpy as np
from PIL import Image
import os
import cv2

def train_classifier(data_dir):
    path = [os.path.join(data_dir,f) for f in os.listdir(data_dir)]
    faces = []
    ids =[]
    for image in path:
        img = Image.open(image).convert('L')
        imageNp =np.array(img,'uint8')
        id = int(os.path.split(image)[1].split(".")[1])

        faces.append(imageNp)
        ids.append(id)
    ids=np.array(ids)


#train the clssifier and save
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces,ids)
    clf.write("clasifier.xml")

train_classifier("data")