# -*- coding: cp936 -*-
import urllib
import json
import re

class JD(object):
    def __init__(self,url):
        self.url = url
        self.req = urllib.urlopen(self.url)
        self.content = self.req.read()
    def info(self):
        pattern = re.compile(r'compatible: true,(.*?};)',re.S)
        info = re.findall(pattern,self.content[0])
        return info
    def skuid(self):
        product_info = self.info()
        pattern_skuid = re.compile(r'skuid:(.*?),')
        skuid = re.findall(pattern_skuid,product_info[0])
        return skuid
    def get_name(self):
        product_info = self.info()
        pattern_name = re.compile(r"name: '(.*?)',")
        name = re.findall(pattern,product_info)
        return name.decode('unicode-escape')
    def get_price(self):
        skuid = self.skuid()
        name = self.get_name()
        url = 'http://p.3.cn/prices/mgets?skuIds=J_' + skuid + '&type=1'
        price_json = json.load(urllib.urlopen(url))[0]
        if price_json['p']:
            price = price_json['p']
        return price
    def get_comment(self):
        
        skuid = self.skuid()
        url = 'http://club.jd.com/review/' + skuid + '-1-1-0.html'
        conment = urllib.urlopen(url).read()
        pattern_2 = re.compile('</span>.*?</div>.*?<div class="comment-content">.*?<dd>(.*?)</dd>.*?<div class="dl-extra">.*?<dl>',re.S)
        pattern_1 = re.compile('全部评价.*?<em>\((.*?).</em></a>',re.S)
        pattern = re.compile('<dt>心.*?</dt><dd>(.*?)</dd>',re.S)
        comment_count = re.findall(pattern_1,conment)
        comments = re.findall(pattern,conment)
        print "全部评论："
        print comment_count[0]
if __name__ == '__main__':
    url = 'http://item.jd.com/1221861.html'
    jp = JD(url)
    print jp.get_price()
    jp.get_comment()








        

    
