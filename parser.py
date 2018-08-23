# encoding=utf8
import requests
import re
from html.parser import HTMLParser


class Myparser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.houses = []
        self.new_house_indicator = False
        self.li_indicator = False
        self.h3_indicator = False
        self.i_indicator = False
        self.p_star_indicator = False
        self.p_location_indicator = False
        self.p_location_span_indicator = False

        # holders
        self.holder_html = ''
        self.holder_name = ''
        self.holder_price = ''
        self.holder_star = ''
        self.holder_location = ''

    def handle_starttag(self, tag, attrs):
        if not self.new_house_indicator:
            return

        if tag == 'li':
            str_attrs = dict(attrs)
            if str_attrs['class'] == '':
                self.li_indicator = True
        if not self.li_indicator:
            return

        # html info
        if tag == 'a':
            str_attrs = dict(attrs)
            p = re.compile(r'\d+')
            if str_attrs.__contains__('href'):
                the_html = p.findall(str_attrs['href'])
            elif str_attrs.__contains__('data-href'):
                the_html = p.findall(str_attrs['data-href'])
            else:
                raise ValueError
            self.holder_html = ''.join(the_html)

        if tag == 'h3':
            self.h3_indicator = True

        if tag == 'i':
            self.i_indicator = True

        # star info
        if self.p_star_indicator:
            if tag == 'span':
                str_span = dict(attrs)
                if str_span.__contains__('star'):
                    self.holder_star = str_span['star']
                    self.p_star_indicator = False
        if tag == 'p':
            str_p = dict(attrs)
            if str_p['class'] == 'x-intro':
                self.p_star_indicator = True

        # location info
        if self.p_location_indicator:
            if tag == 'span':
                str_span = dict(attrs)
                if not str_span.__contains__('class'):
                    self.p_location_span_indicator = True
        if tag == 'p':
            str_p = dict(attrs)
            if str_p['class'] == 'fc':
                self.p_location_indicator = True

    def handle_endtag(self, tag):
        if not self.new_house_indicator:
            return
        if tag == 'li' and self.li_indicator:
            if self.holder_price == '':
                self.holder_price = '价格待定'
            out_info = [self.holder_name,
                        self.holder_location,
                        self.holder_price,
                        self.holder_star,
                        self.holder_html]
            self.houses.append(out_info)
            self.reset_info()
            self.li_indicator = False
        if not self.li_indicator:
            return

        if tag == 'i':
            self.i_indicator = False


    def handle_data(self, data):
        if (not self.new_house_indicator) and (not self.li_indicator):
            return

        # name info
        if self.h3_indicator:
            p = re.compile(r'[\u4e00-\u9fa5a-zA-Z0-9]')
            the_name = p.findall(data)
            if not the_name:
                return
            self.holder_name = ''.join(the_name)
            self.h3_indicator = False

        # price info
        if self.i_indicator:
            p = re.compile(r'\d+')
            the_price = p.findall(data)
            if not the_price:
                return
            self.holder_price = ''.join(the_price)
            self.i_indicator = False

        # location info
        if self.p_location_span_indicator:
            p = re.compile(r'[\u4e00-\u9fa5a-zA-Z0-9]')
            the_location = p.findall(data)
            if not the_location:
                return
            self.holder_location = ''.join(the_location)
            self.p_location_span_indicator = False
            self.p_location_indicator = False

        r = 1

    def handle_comment(self, data):
        if re.match(data, ' 新房 begin '):
            self.new_house_indicator = True
            # print(data)
        elif data == ' 新房 end ':
            self.new_house_indicator = False
            # print(data)

    def reset_info(self):
        self.holder_name = ''
        self.holder_location = ''
        self.holder_price = ''
        self.holder_star = ''
        self.holder_html = ''
        return


def houseparser(url):
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,es;q=0.7',
        'Connection': 'keep-alive',
        'Cookie': 'stationOrder=; comareaOrder=; JSESSIONID=aaa2OUBqKzZY-7WqyJSqw; __jsluid=f09451c8196f6cf46422195c17b08306; global_cookie=48a90685-1529759003867-6da7710a; unique_cookie=U_48a90685-1529759003867-6da7710a; mencity=nb; global_wapandm_cookie=37ag93t0porwmvhrhl4rb3v0p2qjirf03rk; __utma=147393320.1250600944.1529758986.1529758986.1529758986.1; __utmc=147393320; __utmz=147393320.1529758986.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt_t0=1; __utmt_t1=1; g_sourcepage=undefined; apptc=2011121762; unique_wapandm_cookie=U_37ag93t0porwmvhrhl4rb3v0p2qjirf03rk*6; __utmb=147393320.14.10.1529758986',
        'Host': 'm.fang.com',
        'Referer': 'https://m.fang.com/xf/nb/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    req = requests.get(url, headers=headers)
    s = req.text
    myparser = Myparser()
    myparser.feed(s)
    myparser.close()
    return myparser.houses


if __name__ == '__main__':
    url = 'https://m.fang.com/xf/nb/'
    houses = houseparser(url)
    print(houses)
