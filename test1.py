import requests
from lxml import etree
import re
import json
from openpyxl import Workbook
import sys
# from pyecharts import Geo

headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}

def get_url_list(keyword, max_page=5):
    # 构造爬取页面列表
    job_url = []
    for i in range(1, max_page + 1):
        print('爬取第{}页......'.format(i))
        temp_url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,' + keyword + ',2,' + \
                   str(i) + '.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
        r = requests.get(temp_url, headers=headers)
        r.encoding = 'gbk'
        html = etree.HTML(r.text)
        url_list = html.xpath(
            '//*[@id="resultList"]/div[position()>3 and position()<54]/p/span/a/@href'
        )
        job_url.extend(url_list)
    return job_url

def get_job_info(job_url):
    job_info = []
    for i, url in enumerate(job_url):
        print('获取第{}个职位......'.format(i+1))
        temp_info = {}
        r = requests.get(url, headers=headers)
        r.encoding = 'gbk'
        html = etree.HTML(r.text)
        try:
            temp_info['title'] = html.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/h1/@title')[0]
            temp_info['cname'] = html.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[1]/a[1]/@title')[0]
            temp_info['salary'] = html.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/strong/text()')[0]
            temp_info['city'] = html.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()')[0].strip().partition('-')[0]
            # 增加一个福利的爬取
            benefit = html.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/div/div/span/text()')
            if benefit:
                temp_info['job_benefit'] = benefit
            else:
                temp_info['job_benefit'] = '无'
            temp_msg = str(html.xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div/p/text()'))
            if temp_msg:
                temp_info['job_msg'] = ''.join(re.split(r"\\xa0|', '|\\u3000", temp_msg))
            else:
                temp_info['job_msg'] = '无'
            temp_info['address'] = html.xpath('/html/body/div[3]/div[2]/div[3]/div[2]/div/p/text()')[-1].strip()
            temp_info['url'] = url
            if temp_info['city'][-1] != '省' and len(temp_info['city']) <= 3:
                job_info.append(temp_info)
            # json_str = json.dumps(temp_info, ensure_ascii=False)
            # f1.write(json_str)
            print(temp_info)
        except:
            pass
    return job_info

# def write_to_excel(job_info):
#     wb = Workbook()
#     sheet = wb.active
#     sheet.append(list(job_info[0].keys()))
#     wb.save()

# def sum_of_province(job_info):
#     res = {}
#     for job in job_info:
#         if job['city'] in res.keys():
#             res[job['city']] += 1
#         else:
#             res[job['city']] = 1
#     return res
#
# def draw_map(keyword, sop):
#     geo = Geo(keyword + '招聘信息', keyword, title_color='#fff',
#               title_pos='center', width=1200, height=600)
#     geo.add('', list(sop.keys()), list(sop.valus()),
#             visua_text_color='#fff', symbol_size=15, is_visualmap=True)
#     geo.render()

def main():
    job_url = get_url_list('python', 1)
    job_info = get_job_info(job_url)
    i = 0
    with open('D:\job_spider\job_list.txt', 'w+') as f1:
        for item in job_info:
            f1.write("第{}个职位".format(i+1) + '\n' + '\n')
            i += 1
            for key, value in item.items():
                f1.write(key + ':' + str(value) + '\n')
            f1.write('\n')
    # print(job_info)

if __name__ == '__main__':
    # pass
    main()