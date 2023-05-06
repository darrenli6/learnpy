
from urllib.request import build_opener

from urllib.request import ProxyHandler

proxy=ProxyHandler({'http':'127.0.0.1:7890'})

opener=build_opener(proxy)

url='https://www.baidu.com/'
resp=opener.open(url)
print(resp.read().decode('gbk'))