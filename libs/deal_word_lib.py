# -*-coding:utf8-*-
import os
import sys
import json
import re
import urllib
import requests
import logging
from lxml import etree
from w3lib.html import remove_tags
from collections import OrderedDict
from .dict2xml import dict2xml
from .const import tones,danbishun_dict,num2chinese

LOGGING_FORMAT = '%(asctime)-15s:%(levelname)s: %(message)s'
logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO,
                    filename='working/deal_word_lib.log', filemode='a')

_DIR = os.path.dirname(os.path.abspath(__file__))

# 8400/8600
def to_xml_file(xml_data, filename, encoding="GBK"):
    xml = dict2xml(xml_data).to_xml()
    if not isinstance(xml, etree._ElementTree):
        raise Exception('xml should be a tree object, but get: %s' % type(xml))
    xml.write(filename, pretty_print=True, xml_declaration=True, encoding=encoding)

# 8400
def dealchinesenum(bishunnum):
    bishun_str = str(bishunnum)
    hanzi_str = ''
    if len(bishun_str) == 2:
        for i in range(len(bishun_str)):
            for k, v in num2chinese.items():
                if bishun_str[i] == k:
                    hanzi_str += v[1 - i]
    else:
        for k, v in num2chinese.items():
            if bishun_str == k:
                hanzi_str += v[0]

    return bishun_str + ';' + hanzi_str

# 8400/8600
def dealJsonDict(json_str):
    if len(json_str) > 0:
        json_dict = json.loads(json_str)
        return json_dict
    return dict()


# 8400
def dealShiyiZuci(shiyi_str):
    pattern_A = re.findall("(：.+?)。", shiyi_str)
    if pattern_A:
        for a in pattern_A:
            if '～' in a:
                shiyi_str = shiyi_str.replace(a, '')

    # while True:
    #     shiyi_str_old = shiyi_str
    #     pattern_B = re.findall("(。.+?)。", shiyi_str)
    #     if pattern_B:
    #         for b in pattern_B:
    #             if '～' in b and len(b) < 9:
    #                 shiyi_str = shiyi_str.replace(b, '')
    #     else:
    #         break

    pattern_C = re.findall('(〔.+?〕)',shiyi_str)
    if pattern_C:
        for c in pattern_C:
            if '～' in c and len(c) < 8:
                shiyi_str = shiyi_str.replace(c, '')

    if '～' in shiyi_str:
        shiyi_str_new = ''
        shiyi_list = shiyi_str.split('。')
        for shiyi in shiyi_list:
            shiyi = shiyi.strip()
            if len(shiyi) > 0 and shiyi != '”':
                if '～' not in shiyi:
                    shiyi_str_new += shiyi + '。'
                else:
                    if len(shiyi) > 6:
                        shiyi_str_new += shiyi + '。'
        shiyi_str = shiyi_str_new

    return shiyi_str


# 8400
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

    shiyi_str = remove_tags(dealShiyiZuci(shiyi_str)).replace('。。','。').strip()

    if len(shiyi_str) == 0:
        shiyi_str = '暂未详解'

    # if len(shiyi_str.encode('utf8')) > 1000:
    #     shiyi_list = shiyi_str.split('                                                    ')
    #     sylen = len(shiyi_list)
    #     shiyi_str = '   '.join(shiyi_list[:int(sylen/2)])

    if "”" in shiyi_str and "“" in shiyi_str:
        return shiyi_str
    else:
        return shiyi_str.replace("”", '').replace("“",'')

# 8600
def dealDuoyinzizc(new_dict):
    flag = 1
    for dyzzc in new_dict.values():
        if len(dyzzc.strip()) == 0:
            flag *= 0
    return flag

# 8600
def dealZuci(new_str):
    while True:
        if len(new_str.encode('utf8')) > 1000:
            try:
                new_str = ','.join(new_str.split(',')[:-3])
            except:
                new_str = ','.join(new_str.split(',')[:-1])
        else:
            return new_str

# 8400/8600
def removeXml(OUTPUT):
    for root, dirs, files in os.walk(OUTPUT):
        if len(files) != 0:
            for f in files:
                os.remove(root + f)


if __name__ == '__main__':
    print("hah")

