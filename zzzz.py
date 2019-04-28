import requests

urltest = 'http://data.stats.gov.cn/easyquery.htm?id=zb&dbcode=hgnd&wdcode=zb&m=getTree'

a  = requests.get(urltest).text
print(a)



# hello world