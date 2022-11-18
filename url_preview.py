#!/usr/bin/env python3

import re

""" URL 파싱 데이터 """
url_parse = None

""" 메타 테그 추출 정규표현식 """
p_meta = re.compile("<meta .*?[\" /]>")

""" 메타 테그의 property 값 추출 """
p_property = re.compile("property=\"[^\"]*?\"")

""" 메타 테그의 content 값 추출 """
p_content = re.compile("content=\"[^\"]*?\"")

""" iframe 테그 추출 """
p_iframe = re.compile("<iframe .*?>")

""" iframe의 src 값 추출 """
p_src = re.compile("src=\"[^\"]*?\"")

""" 정규표현식으로부터 값 추출하는 메쏘드들 """
def get_meta_tag(line):
    extracted = p_meta.findall(line)
    return extracted

def get_property(line):
    property = p_property.findall(line)
    if len( property ) == 0:
        return None
    return property[0][len("property="):].replace('\"', '').strip()

def get_content(line):
    content = p_content.findall(line)
    if len( content ) == 0:
        return None
    return content[0][len("content="):].replace('\"', '').strip()

def get_iframe_tag(line):
    extracted = p_iframe.findall(line)
    return extracted

def get_src(line):
    srcs = p_src.findall(line)
    if len(srcs) == 0:
        return None
    return srcs[0][len("src="):].replace('\"', '').strip()

""" 라인별로 값을 추출한다. """
def parse_line(line, dic):
    #print("Line :", line)
    extracted = get_meta_tag(line)
    for item in extracted:
        #print("item :", item)
        property = get_property(item)
        content = get_content(item)
        if property != None:
            print("property : ", property)
            print("content : ", content)
            dic[property] = content

    extracted = get_iframe_tag(line)
    for item in extracted:
        print("iframe tag :", item)
        src = get_src(item)
        if src == None:
            continue
        print("src :", src)

        if src.startswith("/"):
            """ 상대 경로 추가 파싱(재귀호출) """
            new_url = "{}://{}{}".format(url_parse[0], url_parse[1],src)
            print("new url :", new_url)
            html = get_text_from_url(new_url)
            #print("new content :", html)
            parse(html, dic)
        elif src.startswith("https://"):
            """ 완전한 URL일 경우 추가로 파싱(재귀호출) """
            new_url = src
            print("new url :", new_url)
            html = get_text_from_url(new_url)
            #print("new content :", html)
            parse(html, dic)

""" 파싱하기 """
def parse(html, dic):
    if type(html) is str:
        parse_line(html, dic)
    elif type(html) is list:
        for line in html:
            parse_line(line, dic)

    return dic

""" URL에서 텍스트 읽어오기 """
def get_text_from_url(url):
    global url_parse
    import urllib.parse
    url_parse = urllib.parse.urlparse(url)
    print(url_parse)
    response = get_from_url(url)
    if not response:
        return None

    encodes = [ "utf-8", "euc-kr", "KSC5601", "cp949" ]
    for enc in encodes:
        try:
            print("Try to decode with {}".format(enc))
            return response.decode(enc)
        except:
            print("Failed!")

""" URL에서 읽어오기 """
def get_from_url(url):
    import urllib.request
    print("get_from_url({})".format(url))
    try:
        req = urllib.request.Request(url)
#        req = urllib.request.Request(url, 
#                headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(url, timeout=10)
        return response.read()
    except:
        print("Cannot open URL : '{}'".format(url))
        return None

def post_from_url(url, data):
    import requests
    print("post_from_url({}, data={})".format(url, data))
    try:
        req = requests.post(url, data)
        return req.content
    except:
        print("Cannot open URL :", url)
        return None

""" URL에서 이미지 읽어보기 """
def get_image_from_url(url):
    return get_from_url(url)

""" 파일에서 읽어오기 """
def read_file(filename):
    return open(filename, 'r').readlines()

""" dic로부터 preview 만들기 """
def make_preview(dic):
    preview = ""
    preview = preview + "{{% assign preview_image_url = '{}' %}}".format(dic['og:image'])
    preview = preview + "{{% assign preview_url = '{}' %}}".format(url)
    preview = preview + "{{% assign preview_title = '{}' %}}".format(dic['og:title'])
    preview = preview + "{{% assign preview_description = '{}' %}}".format(dic['og:description'])
    preview = preview + "{% include body-preview.html %}"
    return preview

if __name__ == '__main__':
    lines = None

    import sys
    import os
    if len(sys.argv) > 1:
        """ 인자로 실행되었을 경우 """
        if sys.argv[1].startswith("https://"):
            url = sys.argv[1]
            """ URL 형식이면 URL에서 가져옴 """
            lines = get_text_from_url(url)
        elif os.path.isfile(sys.argv[1]):
            """ 존재하는 파일이면 파일에서 가져옴 """
            lines = read_file(sys.argv[1])
    elif os.path.isfile("sample3.html"):
        lines = read_file("sample3.html")

    """ 파일이 있으면 열어서 파싱 """
    if lines:
        dic = {}
        parse(lines, dic)
        print(dic)
        for key in dic:
            if key == "og:image" and dic[key] != "":
                print("이미지 확인")
                get_image_from_url(dic[key])
    else:
        print("Cannot read data")
