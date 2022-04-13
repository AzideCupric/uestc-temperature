import re

str1='https://jzsz.uestc.edu.cn/epidemic2/?sessionId=28d9a98b-3ee4-4812-bfe8-8817c8068a5b#/pages/epidemic/everyDay/everyDay'
restr=r'^[A-Za-z0-9]{8}(-[A-Za-z0-9]{4}){3}-[A-Za-z0-9]{12}'
result=re.search(restr,str1)
print(result.group(0))
