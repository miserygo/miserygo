from lxml import etree
from urllib import parse
from web.utils.sqlalchemy import Block,Hot,createdatable
import aiohttp
import asyncio
import re
from concurrent.futures import ThreadPoolExecutor
from scrapyrank.utils.Wangyiyun import Wangyiyun, Cracker
from django.shortcuts import HttpResponse
threadpool=ThreadPoolExecutor(100)

class CrawlData:
    def __init__(self):
        self.urls={
            # 'V3EX':'https://www.v2ex.com/?tab=hot',
            # 'Github':'https://github.com/trending',
            'WeiBo':'https://s.weibo.com/top/summary',
            'ZhiHu':'https://www.zhihu.com/hot',
            # 'Wangyiyun':'https://music.163.com/discover/toplist?id=991319590',
            'Hupu':'https://bbs.hupu.com/all-gambia',
        }
        self.headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        }

    async def getConn(self,name):
        url=self.urls.get(name)
        async with aiohttp.ClientSession(headers=self.headers)as session:
            async with session.get(url)as resp:
                if resp.status==200:
                    soup=etree.HTML(await resp.text())
                    return soup
                else:
                    print('获取{}失败'.format(name))
                    return None


    async def GetZhiHu(self):
        url = 'https://www.zhihu.com/hot'
        self.headers['cookie']='d_c0="AHCi4LryqQ2PToaeQznypeFe3yaTeUbhuU4=|1527523327"; _zap=b61283cf-6fa0-494b-a271-86268feb621b; capsion_ticket="2|1:0|10:1591158881|14:capsion_ticket|44:NDIwMzk4YmZhOGQ2NGI4ODhiZGEyNjQwZTY1ZjdiODA=|263e396d77db32cfa58fb9db346db179d03e0b4e048a1ea3db8e8e66394c88fe"; r_cap_id="MDE5Y2M4MjRjNjc4NGMzNThjYWZiOGM0MmM0MWNkMGE=|1591158886|ac67a793f19df00b6f2f86fcf8865e811a982873"; cap_id="M2Y2NzFiMzc1OGI3NDJlYjgyMGIwNGY2Y2JjMWM3NWM=|1591158886|a04859028eb569e33a610d1a2317d7cc9ff85464"; l_cap_id="ZWRjMzQzMzY0ZjAzNGYwOTg1MDNhMGE4ZjQ3OGU4NGU=|1591158886|4f23da901b96ecba08290c0d3aa3f22b0af51983"; z_c0=Mi4xS3RmdUFRQUFBQUFBY0tMZ3V2S3BEUmNBQUFCaEFsVk5ibmJFWHdENFZBU2dnU3R4YVBWSExLM3pHMkhBMjh1ODR3|1591158894|81d3e05854a15e982c9fc6c4d4d065e08336b1cc; q_c1=022896cb1b114235a330b7942d650ef1|1591271431000|1527523327000; _xsrf=386b8fef-03c1-4997-a644-ddc768c7b937; tst=h; SESSIONID=q6dwUtLgzUuTbJ3Tb87krl1qZwYWAijnFW6wLj0QX3V; JOID=U1wSAktx1Jj036AILHEggVCvwWc7BeH6govRR00KhO6mvOs-e7B4e6rbpg0r-drbV4ye_2Oo6dVdBdH5DEHYU1I=; osd=UVsdCk5z05f82qIPI3klg1egyWI5Au7yh4nWSEUPhumptO48fL9wfqjcqQUu-93UX4mc-Gyg7NdaCtn8DkbXW1c=; tshl=; KLBRSID=ca494ee5d16b14b649673c122ff27291|1592044016|1592043970; unlock_ticket="ABCMM3mqeggXAAAAYQJVTfiw5F5F0W8osgDSp88icnmkyYNu4hMsTg=="'
        async with aiohttp.ClientSession(headers=self.headers)as session:
            async with session.get(url)as resp:
                if resp.status==200:
                    soup=etree.HTML(await resp.text())
                else:
                    print('获取{}失败'.format(url))
                    return None
        items = soup.xpath('//div[@class="HotList-list"]/section')
        for item in items:
            title = item.xpath('div[2]/a/h2/text()')[0]
            content = item.xpath('div[2]/a/p/text()')
            url = item.xpath('div[2]/a/@href')[0]
            if content:
                content=content[0].strip()
            else:
                content=''
            print(title, url, content)
            threadpool.submit(Hot.addHot, title=str(title), url=str(url), block='ZhiHu', content=content)
            #await Hot.addHot(title=str(title), url=str(url), block='ZhiHu', content=content)

    async def GetWeiBo(self):
        soup = await self.getConn('WeiBo')
        items = soup.xpath('//div[@class="data"]/table/tbody/tr')
        for item in items:
            title = item.xpath('td[2]/a/text()')[0]
            url = parse.urljoin('https://s.weibo.com',item.xpath('td[2]/a/@href')[0])
            print(title, url)
            threadpool.submit(Hot.addHot, title=str(title), url=str(url), block='WeiBo', content='')
            #await Hot.addHot(title=str(title), url=str(url), block='WeiBo', content='')

    async def GetWangyiyun(self):
        soup = await self.getConn('Wangyiyun')

        lis = soup.xpath("//*[@class='f-hide']")[0]
        print(lis)
        for li in lis:
            title = li.xpath('./a/text()')[0]
            url = li.xpath('./a/@href')[0]
            id = re.search('(.*?)\?id=(\d+)', url).group(2)
            print(title, id)
            a = Wangyiyun(id)
            url = a.get()
            threadpool.submit(Hot.addHot, title=str(title), url=str(url), block='Wangyiyun', content='')

    async def GetHupu(self):
        soup = await self.getConn('Hupu')

        items = soup.xpath('//*[@id="container"]/div/div[2]/div[1]/ul//li')
        # print(items)
        for item in items:
            title = item.xpath('./span[1]/a/@title')[0]
            url = item.xpath('./span[1]/a/@href')[0]
            print('111',title, url)
            threadpool.submit(Hot.addHot, title=str(title), url='https://bbs.hupu.com/'+str(url), block='Hupu', content='')
def ExecGetData(spider,value):
    dataType=getattr(spider,"Get"+value)
    return dataType

def main(request):
    # createdatable()
    allData=[
         # 'WeiBo',
         # 'ZhiHu',
         # 'Wangyiyun',
         'Hupu'
    ]
    # loop = asyncio.get_event_loop()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    print("开始抓取{}种数据类型".format(len(allData)))
    spider = CrawlData()
    tasks=[]
    for _,value in enumerate(allData):
        print("开始抓取"+value)
        Block.addBlock(value)
        func=ExecGetData(spider,value)
        tasks.append(func())
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()
    return HttpResponse('ok')

class test:
    name = 'hehe'
if __name__ == '__main__':
    main()