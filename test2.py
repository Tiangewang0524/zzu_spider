import pdfkit

confg = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

# url='http://www16.zzu.edu.cn/msgs/vmsgisapi.dll/vmsglist?mtype=x&lan=203'#一篇博客的url
# pdfkit.from_url(url, 'zzu_index_2.pdf', configuration=confg)
#
pdfkit.from_file('test1111.html', 'test_html_2.pdf', configuration=confg)
# # from_file这个函数是从文件里面获取内容
# # 这有3个参数，第一个是一个html文件，第二个是文生成的pdf的名字，第三个就是khtmltopdf的路径

# from PyPDF2 import PdfFileMerger
# import os
#
# merger = PdfFileMerger()
# file_path = 'D:\\PycharmProjects\\zzu_spider\\test123'
# for pdf in os.listdir(file_path):
#     pdf = file_path + '\\' + pdf
#     print(pdf)
#     merger.append(open(pdf, 'rb'))
#
# merger.write('合并test.pdf')
# print('合并完成')

