import xml.etree.ElementTree as ET
import pandas as pd
import os
import re
import string


filenames = os.listdir("./report_test/")


caption_set = []
for name in filenames:

    if 'xml' in name:
        tree = ET.parse("./report_test/" + name)
        root = tree.getroot()
        #caption

        report = next(root.iterfind("MedlineCitation"))[0][2]


        caption = ''

        if report is None: continue

        for i in range(4):

            if i != 3: continue # only use impressions

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


        caption_set.append(caption)

caption_df = pd.DataFrame({'text':caption_set})
caption_df['index'] = caption_df.index

caption_df.to_csv("caption_text.csv")
