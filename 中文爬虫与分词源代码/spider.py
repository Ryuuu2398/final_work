import requests
from lxml import etree
import asyncio
import aiohttp
import re
import aiofiles
import time
import nest_asyncio
import os
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


nest_asyncio.apply()#我也不懂但这条语句不加不行
obj=re.compile(r'<span class="content-wrap">(?P<title>.*?)</span>.*?<div class="read-content j_readContent" id=".*?">(?P<content>.*?)</div>',re.S)#预先准备正则
bookid='1010868264'#小说的ID

def wordcount():
    with open('wbfx.txt','r') as txt:
        content=txt.read()    #读取文本内容

    #文本预处理，去除无用词汇，只提取中文
    new_data=re.findall('[\u4e00-\u9fa5]+',content,re.S)
    new_data=' '.join(new_data)

    words_list = jieba.lcut(new_data)     # 使用精确模式对文本进行分词

    #去掉单个词，无用词，比如说虚词等等
    with open('stop_words.txt','r',encoding='utf-8') as f:
        stop_words=set()
        stop_words_line=f.read().split('\n')
        for i in stop_words_line:
            stop_words.add(i)
    words=[]
    for i in words_list:
        if i not in stop_words and len(i)>1:
            words.append(i)

    counts = {}     # 通过键值对的形式存储词语及其出现的次数
    cnt=0
    word_2=[]

    for word in words:
        counts[word] = counts.get(word, 0) + 1    # 遍历所有词语，每出现一次其对应的值加 1
        word_2.append(word)
        if len(word) >= 6:      #统计6个及以上长度的词语
            cnt+=1
            
    items = list(counts.items())#将键值对转换成列表
    items.sort(key=lambda x: x[1], reverse=True)    # 根据词语出现的次数进行从大到小排序

    print('出现次数最多的15个词语次数为:')
    for i in range(15):
        word, count = items[i]
        print("{0:<5}{1:>5}".format(word, count))

    print('六个及以上长度词语的数量为:',cnt)


    # 指定云词的模板
    image = np.array(Image.open("input.jfif"))

    # 使用WordCloud进行云词的展示
    wc = WordCloud(font_path="方正少儿简体.TTF",scale=2, mask=image, background_color="white",max_words=2000)
    wc.generate(' '.join(word_2))

    # 绘制,可以不用绘制直接保存图片
    plt.imshow(wc)
    plt.axis("off")
    plt.show()

    # 保存文件
    wc.to_file("output.png")

def createwbfx(n):
    with open('wbfx.txt',mode='w') as fw:
        for i in range(n):
            with open(f'./novel/第{i+1}章.txt',mode='r') as fr:
                fw.write(fr.read())

async def download(no,url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            html=await resp.text()
            result=obj.search(html)#使用正则表达式筛选文本内容
            title=result.group("title")
            content=result.group("content")
            text_row=content.replace(" ","").split('<p>')
            text_row[0]=title
            text='\n'.join(text_row)
            async with aiofiles.open(f'./novel/第{no+1}章.txt',mode='w') as f:
                await f.write(text)
            await print(title,'下载完毕!')            

def main():
    starttime = time.time()
    catalog_url=f'https://book.qidian.com/info/{bookid}/#Catalog'
    #1.访问小说章节目录网站
    proxies={
        "http":None,
        "https":None
    }
    headers={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43"
    }
    resp=requests.get(url=catalog_url,proxies=proxies,headers=headers)
    resp.encoding='utf-8'#避免乱码
    #2.用xpath获取各章节网址
    tree=etree.HTML(resp.text)
    results=tree.xpath(r'//*[@id="j-catalogWrap"]/div[2]/div[1]/ul/li/h2/a/@href')#通过浏览器审查元素定位，然后右键复制xpath，可直接得到章节的路径
    url_list=[]
    for result in results:
        url_list.append('https:'+result)#获取每一章节的URL
    #3.使用异步协程下载各章节
    if not os.path.exists(r'./novel'):
        os.mkdir(r'./novel')
    task = [asyncio.ensure_future(download(i,u)) for i,u in enumerate(url_list)]
    asyncio.run(asyncio.wait(task))
    print('所有章节下载完毕')
    endtime = time.time()-starttime
    print('共耗时',endtime,'秒')
    #4.将各章节合并为wbfx.txt
    createwbfx(len(url_list))
    #5.分词，并生成词云
    wordcount()


if __name__ == '__main__':
    main()

