import requests
from lxml import etree
import re
# 敏感词过滤类，AC自动机
import Ac_auto

headers = {
    'User-Agent':
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;'
}


# 查找所有栏目的url，并保存
def all_urls_list():
    urls_list = []
    url = 'http://news.zzu.edu.cn/'
    r = requests.get(url, headers=headers)
    r.encoding = 'UTF-8'
    html = etree.HTML(r.text)
    # 郑大共有8个栏目
    for i in range(1, 9):
        news_heading_url = html.xpath('//*[@id="mytop_3"]/a[' + str(i) + ']/@href')
        news_heading_url = ''.join(news_heading_url)
        urls_list.append(news_heading_url)
    # print(urls_list)
    # 添加郑大通知公告url(单独的)：
    extra_url = 'http://www16.zzu.edu.cn/msgs/vmsgisapi.dll/vmsglist?mtype=m&lan=101,102,103'
    urls_list.append(extra_url)

    return urls_list


# 查找每个栏目下的url，并保存
def get_url_list(url):
    url_list = []
    r = requests.get(url, headers=headers)
    r.encoding = 'UTF-8'
    html = etree.HTML(r.text)

    # 查找最大页数
    page = html.xpath('//*[@id="bok_0"]/div[@class="zzj_4"]/text()[1]')
    page = ''.join(page)
    # print(page)
    search_obj = re.search(r'分\d+页', page)
    #print(search_obj.group())
    page = re.search(r'\d+', search_obj.group())
    # print(page.group())
    max_page = int(page.group())

    for i in range(1, max_page + 1):
        # print('爬取网上新闻的第{}页......'.format(i))
        temp_url = url + '&tts=&tops=&pn=' + str(i)
        url_list.append(temp_url)
    return url_list


# 查找每一页url里的新闻的url，并保存
def get_url_info(url_list):
    url_info = []
    # 新闻数累加器
    sum_i = 0

    # 获取新闻栏目名
    r = requests.get(url_list[0], headers=headers)
    r.encoding = 'UTF-8'
    html = etree.HTML(r.text)
    news_heading = html.xpath('//*[@id="bok_0"]/div[@class="zzj_3"]/text()')
    news_heading = ''.join(news_heading)

    for i, url in enumerate(url_list):
        for j in range(0, 50):
            # 将新闻标题+内容整合，保存为字典
            temp_info = {}
            r = requests.get(url, headers=headers)
            r.encoding = 'UTF-8'
            html = etree.HTML(r.text)
            tips = '获取{}栏目下第{}页第{}条新闻，总第{}条新闻......'.format(news_heading, i + 1, j + 1, sum_i + 1)
            print(tips)
            try:
                xpath_temp = '//*[@id="bok_0"]/div[@class="zzj_5"]/div[' + str(1 + j * 2) + ']/a/'
                temp_info['title'] = html.xpath(xpath_temp + 'span/text()')[0]
                # 新闻的具体url
                news_url = html.xpath(xpath_temp + '@href')
                news_url = ''.join(news_url)
                # print(news_url)
                # 引入tips, 查找爬虫出错未爬取到的空的新闻内容
                temp_info['content'] = get_url_content(news_url, tips)
                print(temp_info)
                url_info.append(temp_info)
            except:
                continue
            sum_i += 1
    return url_info


# 获取具体一条新闻的内容
def get_url_content(news_url, tips):
    r = requests.get(news_url, headers=headers)
    r.encoding = 'UTF-8'
    sub_html = etree.HTML(r.text)
    # 对内容做处理，删除空格换行转义等等字符，并进行关键词校验屏蔽
    # 关键字的校验屏蔽。（关键字：指的是反动言论，不文明词汇）
    content = sub_html.xpath('//*[@id="bok_0"]/div[@class="zzj_5"]//text()')
    content = ''.join(content)
    content = re.sub(r'\s', '', content)

    # print(content)
    content = sensitive_word_filter(content)

    # 如果出现空的内容，输出具体出错的新闻位置并生成txt
    if content == '':
        with open('C:/Users/mcgra/Desktop/spider_error.txt', 'a+') as f1:
            f1.write(tips)
            f1.write('\n')

    return content


# 敏感词过滤
def sensitive_word_filter(content):
    ah = Ac_auto.ac_automation()
    path = 'sensitive_words.txt'
    ah.parse(path)
    content = ah.words_replace(content)
    # text1 = "新疆骚乱苹果新品发布会"
    # text2 = ah.words_replace(text1)
    # print(text1)
    # print(text2)

    return content


def main():
    # 郑大新闻网所有的栏目链接
    all_urls = all_urls_list()
    for url in all_urls:
        url_list = get_url_list(url)
        news_info = get_url_info(url_list)
        print(news_info)


if __name__ == '__main__':
    main()
