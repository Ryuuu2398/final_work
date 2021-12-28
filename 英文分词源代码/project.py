import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

pattern=re.compile(r'[A-Za-z]+',re.S)

def wordscloud(content):
    # 指定云词的模板
    image = np.array(Image.open("picture1.jpg"))

    # 使用WordCloud进行云词的展示
    wc=WordCloud(
    # font_path为字体文件的路径
    font_path="BAUHS93.TTF",

    # scale为按比例放大或者缩小生成的图片。例如1.5表示图片放大为原来的1.5倍，默认为1
    scale=5,

    # mask表示背景图片，如果不没有背景图片，那这个可以省略
    mask=image,

    # background_color为背景颜色，默认为黑色，可以省略
    background_color="white",

    # width为词云生成的图片宽度，默认为400
    width=800,

    # height为词云生成的图片高度，默认为200
    height=766,

    # max_words图片上显示的最大词语的个数，默认为200
    max_words=3000,

    # max_font_size为最大字体的大小
    max_font_size=100,

    # min_font_size为最小字体大小,默认为4
    min_font_size=2)
    wc.generate(content)

    # 绘制
    plt.imshow(wc)
    plt.axis("off")
    plt.show()

    # 保存文件
    wc.to_file("output.png")

def wordscount(words):
    counts = {}     # 通过键值对的形式存储词语及其出现的次数
    cnt=0
    word_2=[]

    for word in words:
        counts[word] = counts.get(word, 0) + 1    # 遍历所有词语，每出现一次其对应的值加 1
        word_2.append(word)
        if len(word) >= 6:    #统计6个及以上长度的词语
            cnt+=1
            
    items = list(counts.items())#将键值对转换成列表
    items.sort(key=lambda x: x[1], reverse=True)    # 根据词语出现的次数进行从大到小排序

    print('出现次数最多的15个单词次数为:')
    for i in range(15):
        word, count = items[i]
        print("{0:<15}{1:>5}".format(word, count))

    print('六个及以上字母的单词的数量为:',cnt)

def main():
    with open('../wbfx.txt','r',encoding='utf-8') as f:
        words_list=pattern.finditer(f.read())
        word_list=[]

        for words in words_list:
            word_list.append(words.group().lower())

        print(word_list)
        wordscount(word_list)
        wordscloud(' '.join(word_list))

if __name__ == '__main__':
    main()