import xml.etree.ElementTree as ET
import json
from skimage import novice
import random
import os
import re
import string
random.seed(123)

result=[]
filenames = os.listdir("./test/")
image_id=0
caption_id=0

for name in filenames:
    if 'xml' in name:

        tree = ET.parse("./test/" + name)
        root = tree.getroot()
        #caption
        # caption

        report = next(root.iterfind("MedlineCitation"))[0][2]

        caption = ''

        if report is None: continue

        for i in range(4):

            if i != 3: continue  # only use impressions

            text = report[i].text
            if text is None: continue

            text = re.sub('None.', '', text)
            text = re.sub('x+|X+', '', text)
            text = re.sub('[+\.\!\-\/_,$%^*(+\"\')]+', '', text)
            text = text.lower()
            text = text.translate(str.maketrans('', '', string.punctuation))
            text.strip()
            if len(text) != 0:
                caption = caption + text + ' '

        #figure
        img=root.iterfind("parentImage")
        image=[]
        for a in img:
            num=random.random()
            image_id+=1
            filename=a[2][0].text
            filename=filename[filename.rfind('/')+1:][:-3]+'png'
            if not os.path.exists('./images/'+filename):
                continue
            picture = novice.open('./images/'+filename)
            width,height = picture.size

            result.append([image_id,caption_id,filename,width,height,caption,num>0.7])


train = 0
val = 0
traindic={'images':[],'annotations':[]}
testdic={'images':[],'annotations':[]}
for r in result:
    if r[6]:
        dic=testdic
        val += 1
    else:
        dic=traindic
        train += 1
    img={'file_name':r[2],'height':r[4],'width':r[3],'id':r[0]}
    cap={'image_id':r[0],"id":r[1],"caption":r[5]}
    dic['images'].append(img)
    dic['annotations'].append(cap)

json.dump(traindic,open('./impression_train.json','w'))
json.dump(testdic,open('./impression_val.json','w'))

print(train)
print(val)
