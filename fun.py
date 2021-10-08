import requests
from Crypto.Cipher import DES3
import base64
import json


key = b'ED^QcS0j7j@I6UQMQBupjrgD'
iv = b'01234567'


def des3encode(text):
    #desede/CBC/PKCS5Padding加密
    #PKCS5Padding
    #字符串长度需要是8的倍数
    BS = 8
    pad = lambda s: s + (BS - len(s.encode()) % BS) * chr(BS - len(s.encode()) % BS)
    unpad = lambda s : s[0:-ord(s[-1])]

    #text也需要encode成bytearray
    plaintext = pad(text).encode()

    #使用MODE_CBC创建cipher
    cipher = DES3.new(key, DES3.MODE_CBC, iv)

    #加密
    result = cipher.encrypt(plaintext)

    #base64 encode
    result = (base64.b64encode(result)).decode()

    return result

def des3decode(text):
    #desede/CBC/PKCS5Padding解密
    #PKCS5Padding
    #字符串长度需要是8的倍数
    BS = 8
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    unpad = lambda s : s[0:-ord(s[-1])]

    #text也需要encode成bytearray
    plaintext = pad(text).encode()

    #使用MODE_CBC创建cipher
    cipher = DES3.new(key, DES3.MODE_CBC, iv)

    #base64 decode
    plain_base64 = base64.b64decode(text)

    #解密
    decrypt_text = cipher.decrypt(plain_base64)

    #截取
    result = unpad(decrypt_text.decode("utf-8"))

    return result

def do_post(data):
    headers = {
        'shareType': 'enjoy_link|ghome|5.6.6',
        'User-Agent': 'enjoy_link|ghome|5.6.6',
    }
    url = "https://ienjoys.mobi/enjoylink/ghome/topicThird/getTopicList.do"
    res = requests.post(url=url, data=data, headers=headers)
    print(res.status_code)
    # print(res.text)
    return res.text

# s = '{"encrypt":true,"code":10000,"desc":"请求执行成功！","rts":"0000000000","sign":null,"result":[]}'
# enstr = des3encode(s).replace('+','-').replace('/','_')
# print(enstr)
# destr = des3decode(enstr.replace('-','+').replace('_','/'))
# print(destr)

data = '{"businessType":"PROJECT","pageNo":1,"type":"300","projectCode":"51010001","head":{"deviceId":"15d5a440-3b06-30f5-bb27-684d872d1ccd","timestamp":1633524248180,"sessionId":"ee08511509b8404c88f4c70a8607105b","macId":"502B73D424DD","deviceInfo":"","token":"d199d602f906fc8d496cbd7697355959","userId":"2311522"},"pageSize":10}'
en_data = des3encode(data).replace('+','-').replace('/','_')

res = do_post(en_data)
de_str = des3decode(res.replace('-','+').replace('_','/'))

base_res = json.loads(de_str)
vlist = base_res.get('result')
for l in vlist:
    print('nickName:',l.get('nickName'))
    print('content:',l.get('content'))
    print('createDate:',l.get('createDate'))
    print("*"*80)