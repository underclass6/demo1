# coding=gbk

import re
import requests
import string
from urllib.request import urlopen
from urllib.parse import quote
import threading
import queue
import time

class Consumer(threading.Thread):
	def __init__(self, process):
		super().__init__()
		self.process = process
	
	# ��дrun����
	def run(self):
		self.process()

def process():
	global picture_url, url_queue
	while True:
		if not url_queue.empty():
			pic_url = url_queue.get()
			if pic_url is None:
				break
			filename = re.search(r'/\d(.*?)\d\.', pic_url)
			try:
				picture = requests.get(pic_url, timeout=10)
			except requests.exceptions.ConnectionError:
				print("ͼƬ������!")
			if filename:
				f = open('C:/Users/58416/Desktop/��ʱ���ص�ͼƬ/' + (filename.group())[-4:-1] + '.jpg', 'wb')
				f.write(picture.content)
				f.close()
			time.sleep(1)
			url_queue.task_done()


want = input('��ӭʹ�ö��߳�ͼƬ������ \\^_^/\n��������Ҫ�������ص�ͼƬ���ƣ�')
thread_num = int(input('�����߳���Ŀ��'))
url = quote('http://image.baidu.com/search/flip?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1525854041746_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&ctd=1525854041747%5E00_1905X898&word=' + want, safe=string.printable)
response = urlopen(url)
html = response.read().decode('utf-8')
picture_url = re.findall(r'\"objURL\":\"(.*?)\",', html, re.S)

url_queue = queue.Queue(len(picture_url)) # ����ͼƬurl�Ķ���
consumers = [] # �����������߳�
for url in picture_url:
	url_queue.put(url)
for i in range(thread_num):
	consumer = Consumer(process)
	consumer.start() # �߳̿�ʼ��������
	consumers.append(consumer)
url_queue.join() # �������߳�ֱ���������������񱻴������

# ����������ɺ���ֹ�߳�
for i in range(len(picture_url)):
	url_queue.put(None)
for consumer in consumers:
	consumer.join()

print('������ϣ�')
