import re
import requests
import string
from urllib.request import urlopen
from urllib.parse import quote
want = input('请输入需要批量下载的图片名称：')
max_num = input('希望下载多少张图片：')
url = quote('http://image.baidu.com/search/flip?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1525854041746_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&ctd=1525854041747%5E00_1905X898&word=' + want, safe=string.printable)
response = urlopen(url)
html = response.read().decode('utf-8')
#html = requests.get(url).text
picture_url = re.findall(r'\"objURL\":\"(.*?)\",', html, re.S)
num = 0
for pic_url in picture_url:
    if num >= int(max_num):
        break
    try:
        picture = requests.get(pic_url, timeout=10)
    except requests.exceptions.ConnectionError:
        print("图片不存在!")
    f = open('/home/underclass/图片/' + str(num) + '.jpg', 'wb')
    f.write(picture.content)
    f.close()
    num += 1
print('下载完毕！')
