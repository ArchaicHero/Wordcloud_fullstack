# Start with loading all necessary libraries
import numpy as np
import pandas as pd
from PIL import Image
from wordcloud import WordCloud, STOPWORDS

import matplotlib.pyplot as plt
WIDTH = 1920
HEIGHT = 1080

df = pd.read_csv("../Assets/winemag-data-130k-v2.csv")
text = " ".join(review for review in df.description)

stopwords = set(STOPWORDS)
stopwords.update(["drink", "now", "wine", "flavor", "flavors"])

mask = np.array((Image.open("../Assets/wine_mask.png")).resize((WIDTH, HEIGHT)))
# convert format from dark image to white image for masking effect
for row in range(len(mask)):
    for col in range(len(mask[row])):
        for n in range(len(mask[row][col])):
            if mask[row][col][n] <= 2:
                mask[row][col][n] = 255

wc = WordCloud(width=WIDTH, height=HEIGHT, max_words=200, mask=mask, stopwords=stopwords, contour_width=2,
               contour_color='firebrick')

wc.generate(text)

wc.to_file("../output/wine.png")

# show
plt.figure(figsize=[20, 10])
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.show()
