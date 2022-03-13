

from faker import Faker
import os
import random
import csv
from utils import DATA_STORE_DIR


fake = Faker()

blogPostFile = os.path.join(DATA_STORE_DIR, "blog_posts.csv")

f = open(blogPostFile, 'w', newline='')

writer = csv.writer(f)

postCount = 100
postStatus = ["Posted", "Draft", "Deleted"]
headerColumns = ['id', 'author', 'article', 'post_date', 'content', 'status', 'like_count', 'commnet_count' ]

writer.writerow(headerColumns)

for i in range(postCount):
    id = "p"+str(i+1)
    author = fake.name()
    article = fake.word() + " " + fake.word() + " " + fake.word()
    post_date = fake.date()
    content = fake.text().split("\n")
    content = ''.join(content)
    # print(content)
    # input()
    status = random.choice(postStatus)
    like_count = random.randint(1,100)
    comment_count = random.randint(1,100)
    dataRow = [str(id), str(author), str(article).title(), str(post_date), str(content), str(status), str(like_count), str(comment_count)]
    writer.writerow(dataRow)