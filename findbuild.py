import builtwith

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

print(builtwith.parse(url='https://www.bilibili.com',
                      headers=headers))

