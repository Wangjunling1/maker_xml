# -*-coding:utf8-*-
import os
import re
import logging
from lxml import etree
from w3lib.html import remove_tags
from .dict2xml import dict2xml
from .const import tones,danbishun_dict,num2chinese,num3chinese

# LOGGING_FORMAT = '%(asctime)-15s:%(levelname)s: %(message)s'
# logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO,
#                     filename='working/deal_phrase_lib.log', filemode='a')

_DIR = os.path.dirname(os.path.abspath(__file__))

# 1400/4300
def to_xml_file(xml_data, filename, encoding="GBK"):
    xml = dict2xml(xml_data).to_xml()
    if not isinstance(xml, etree._ElementTree):
        raise Exception('xml should be a tree object, but get: %s' % type(xml))
    xml.write(filename, pretty_print=True, xml_declaration=True, encoding=encoding)


# 1400/4300
def dealchinesenum(bishunnum):
    bishun_str = str(bishunnum)
    hanzi_str = ''
    if len(bishun_str) == 2:
        for i in range(len(bishun_str)):
            for k, v in num3chinese.items():
                if bishun_str[i] == k:
                    hanzi_str += v[1 - i]
    else:
        for k, v in num3chinese.items():
            if bishun_str == k:
                hanzi_str += v[0]

    return bishun_str + '字;' + hanzi_str + '字'


# 1400
def getShiyiStr(shiyi_dict):
    shiyi_str = ''
    for k,v in shiyi_dict.items():
        shiyi_str += v
    return shiyi_str


# 1400/4300
def dealshiyi(shiyi_str):
    shiyi_str = re.sub(r'笔画数：.*?；部首：.*?；笔顺编号：\d{0,100}', '', shiyi_str) \
        .replace('【动】', '动词 ') \
        .replace('【名】', '名词 ') \
        .replace('【副】', '副词 ') \
        .replace('【形】', '形容词 ') \
        .replace('【量】', '量词 ') \
        .replace('①', '1.') \
        .replace('②', '2.') \
        .replace('③', '3.') \
        .replace('④', '4.') \
        .replace('⑤', '5.') \
        .replace('⑥', '6.') \
        .replace('⑦', '7.') \
        .replace('⑧', '8.') \
        .replace('⑨', '9.') \
        .replace('⑩', '10.')\
        .replace('\n','').replace('\t','').strip()\
        .replace('                                                    ','  　')
    kuohao_p = re.findall('\((.+?)\)', shiyi_str)
    if kuohao_p:
        for kh in kuohao_p:
            shiyi_str = shiyi_str.replace('(' + kh + ')', '')
    kuo_p = re.findall('（(.+?)）', shiyi_str)
    if kuo_p:
        for kp in kuo_p:
            shiyi_str = shiyi_str.replace('（' + kp + '）', '')

    # 简单粗暴
    # if len(shiyi_str.encode('utf8')) > 1000:
    #     shiyi_str = shiyi_str[:1000]

    flag_tag = 0
    if len(shiyi_str.encode('utf8')) > 1000:
        while flag_tag < 20:
            shiyi_str = '</p><p>'.join(shiyi_str.split('</p><p>')[:-1])
            if len(shiyi_str.encode('utf8')) < 1000:
                break
            flag_tag += 1

    flag_juhao = 0
    if len(shiyi_str.encode('utf8')) > 1000:
        while flag_juhao < 20:
            shiyi_str = '。'.join(shiyi_str.split('。')[:-1])
            if len(shiyi_str.encode('utf8')) < 1000:
                break
            flag_juhao += 1

    # if flag_juhao >= 10 and flag_tag >= 10 and len(shiyi_str.encode('utf8')) > 1000:
    #     shiyi_str = shiyi_str.split('</p><p>')[0]
    #     shiyi_str = shiyi_str.split('。')[0]

    shiyi_str = remove_tags(shiyi_str).strip()
    if len(shiyi_str) == 0:
        # print('aaa')
        shiyi_str = '暂未详解'

    return shiyi_str.replace('.：','.')


# 1400/4300
def removeXml(OUTPUT):
    for root, dirs, files in os.walk(OUTPUT):
        if len(files) != 0:
            for f in files:
                os.remove(root + f)


# 1400
def dealChuChu(chuchu_str):
    if len(chuchu_str.encode('utf8')) > 1000:
        flag = 0
        while flag < 3:
            chuchu_str = '</p><p>'.join(chuchu_str.split('</p><p>')[:-1])
            if len(chuchu_str.encode('utf8')) < 1000:
                break
            flag += 1
    return remove_tags(chuchu_str.replace('〖出处〗','')).strip()

def dealChuChu_merge(chuchu_str):
    if len(chuchu_str.encode('utf8')) > 1000:
        flag = 0
        chuchu_list = chuchu_str.split('|')
        while flag < 5:
            result = chuchu_list[:-1]
            chuchu_str = '|'.join(result)
            if len(chuchu_str.encode('utf8')) < 1000:
                break
            flag += 1
    return remove_tags(chuchu_str.replace('〖出处〗','')).strip()

if __name__ == '__main__':
    print("hah")

