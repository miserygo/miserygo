import os
from Crypto.Cipher import AES
import requests
import codecs
import base64
import json
import re
import random
from lxml import etree
from . import config
params = '{"ids":"[1299844875]","level":"standard","encodeType":"aac","csrf_token":""}'
url = 'https://music.163.com/discover/toplist?id=991319590'

def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

def getHtml(url,headers,data,timeout=6):
    # ....
    retry_count = 5
    proxy = get_proxy().get("proxy")
    while retry_count > 0:
        try:
            rep = requests.get(url, headers=headers, data=data, timeout=timeout,proxies={"http": "http://{}".format(proxy)})
            # 使用代理访问
            return rep
        except Exception:
            retry_count -= 1
    # 出错5次, 删除代理池中代理
    delete_proxy(proxy)
    return None
class Wangyiyun:
    def __init__(self, id):
        self.url = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token='

        self.params = {"ids": f"[{id}]", "level": "standard", "encodeType": "aac", "csrf_token": ""}
        self.headers = {
            'Referer': 'https://music.163.com/',
            'User-Agent': random.choice(config.USER_AGENTS)
        }

    def get(self):
        data = self.__postRequest()
        if data:
            return data["data"][0]["url"]

    def __postRequest(self, timeout=6):
        cookie = '_ntes_nuid=6237286233ae4227a03b12f7cc6a3494'
        self.headers.setdefault('Cookies', cookie)
        postdata = Cracker.get(self.params)
        # rep = getHtml(self.url, self.headers, postdata)
        rep = requests.post(self.url, headers=self.headers, data=postdata, timeout=6)
        if rep.json()['code'] == 200:
            return rep.json()
        return rep.text


class Cracker():
    modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    nonce = '0CoJUm6Qyw8W8jud'
    pubKey = '010001'

    @classmethod
    def get(cls, text):
        text = json.dumps(text)
        secKey = cls._createSecretKey(16)
        encText = cls._aesEncrypt(cls._aesEncrypt(text, cls.nonce), secKey)
        encSecKey = cls._rsaEncrypt(secKey, cls.pubKey, cls.modulus)
        post_data = {'params': encText, 'encSecKey': encSecKey}
        return post_data

    @classmethod
    def _aesEncrypt(cls, text, secKey):
        pad = 16 - len(text) % 16
        if isinstance(text, bytes):
            text = text.decode('utf-8')
        text = text + str(pad * chr(pad))
        secKey = secKey.encode('utf-8')
        encryptor = AES.new(secKey, 2, b'0102030405060708')
        text = text.encode('utf-8')
        ciphertext = encryptor.encrypt(text)
        ciphertext = base64.b64encode(ciphertext)
        return ciphertext

    @classmethod
    def _rsaEncrypt(cls, text, pubKey, modulus):
        text = text[::-1]
        rs = int(codecs.encode(text.encode('utf-8'), 'hex_codec'), 16) ** int(pubKey, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    @classmethod
    def _createSecretKey(cls, size):
        return (''.join(map(lambda xx: (hex(ord(xx))[2:]), str(os.urandom(size)))))[0:16]


if __name__ == '__main__':
    # a = Wangyiyun()
    # print(a.get())

    # headers = {
    #     'Referer': 'http://music.163.com/',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.32 Safari/537.36',
    #     # 'Host': 'music.163.com',
    #     # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    # }
    # s = requests.session()
    # proxy = {
    #     "http": "120.27.110.143:80",
    # }
    # rep = s.get(url, headers=headers, proxies=proxy)
    # # print(rep.text)
    # tree = etree.HTML(rep.text)
    # lis = tree.xpath("//*[@class='f-hide']")[0]
    #
    # for li in lis:
    #     title = li.xpath('./a/text()')[0]
    #     url = li.xpath('./a/@href')[0]
    #     id = re.search('(.*?)\?id=(\d+)', url).group(2)
    #     print(title, id)
    #
    #     a = Wangyiyun(id)
    #     url = a.get()
    print(get_proxy())
    # print(random.choice(config.USER_AGENTS))