import requests
from lxml import etree
import re
import pdfkit
from PyPDF2 import PdfFileMerger
import os
# 敏感词过滤类，AC自动机
import Ac_auto

# pdfkit配置
confg = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

# 伪装http请求头部
headers = {
    'User-Agent':
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;'
}


def get_url_info(url_list):
    # 新闻数累加器
    sum_i = 0

    # 获取新闻栏目名
    news_heading = 'Test1'

    # 创建文件夹
    # 先判断文件夹是否存在，不存在则创建文件夹
    # now_dir = os.getcwd()
    new_dir = 'D:\\PycharmProjects\\zzu_spider' + '\\' + news_heading
    dir_judge = os.path.exists(new_dir)
    if not dir_judge:
        os.mkdir(new_dir)
        # print(new_dir)

    # 合并pdf
    merger = PdfFileMerger()
    # 对每页的每个新闻做处理
    for i, url in enumerate(url_list):
        # for j in range(0, 50):
        # 将新闻标题+内容整合，保存为字典
        j = 0
        r = requests.get(url, headers=headers)
        r.encoding = 'UTF-8'
        tips = '获取{}栏目下第{}页第{}条新闻，总第{}条新闻......'.format(news_heading, i + 1, j + 1, sum_i + 1)
        print(tips)
        # 引入tips, 查找爬虫出错未爬取到的空的新闻内容
        try:
            raw_html = r.text
            print(raw_html)
            html_filter = sensitive_word_filter(raw_html)
            pdfkit.from_string(raw_html, new_dir + '\\' + tips[2:-6] + '.pdf', configuration=confg)
            # 合并pdf
            pdf_file = new_dir + '\\' + tips[2:-6] + '.pdf'
            merger.append(open(pdf_file, 'rb'))
            print(merger)
            sum_i += 1
        except:
            continue

        with open('test1111' + '.html', 'w+') as f1:
            f1.write(raw_html)
    # 合并pdf
    merger.write(new_dir + '\\' + '合并test.pdf')
    print('{}栏目pdf合并完成'.format(news_heading))


# 获取具体一条新闻的内容
# def get_url_content(news_url, tips):
#     r = requests.get(news_url, headers=headers)
#     r.encoding = 'UTF-8'
#     sub_html = etree.HTML(r.text)
#     # 对内容做处理，删除空格换行转义等等字符，并进行关键词校验屏蔽
#     # 关键字的校验屏蔽。（关键字：指的是反动言论，不文明词汇）
#     content = sub_html.xpath('//*[@id="bok_0"]/div[@class="zzj_5"]//text()')
#     content = ''.join(content)
#     content = re.sub(r'\s', '', content)
#
#     # print(content)
#     content = sensitive_word_filter(content)
#
#     # 如果出现空的内容，输出具体出错的新闻位置并生成txt
#     if content == '':
#         with open('C:/Users/mcgra/Desktop/spider_error.txt', 'a+') as f1:
#             f1.write(tips)
#             f1.write('\n')
#
#     return content


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
    # all_urls = all_urls_list()
    # for url in all_urls:
    #     url_list = get_url_list(url)
    url = ['http://news.zzu.edu.cn/', 'http://www16.zzu.edu.cn/msgs/vmsgisapi.dll/vmsglist?mtype=x&lan=203']
    get_url_info(url)


if __name__ == '__main__':
    main()