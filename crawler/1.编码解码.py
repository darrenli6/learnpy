import urllib.parse

kw ={"wd":"darren李"}

#编码
result =urllib.parse.urlencode(kw)
print(result)

#解码
res =urllib.parse.unquote(result)
print(res)