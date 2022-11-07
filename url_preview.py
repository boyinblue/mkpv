#!/usr/bin/env python3

import urllib.request
import re

p_meta = re.compile("<meta .*?[\" /]>")
p_property = re.compile("property=\"[^\"]*?\"")
p_content = re.compile("content=\"[^\"]*?\"")

p_iframe = re.compile("<iframe .*?>")
p_src = re.compile("src=\"[^\"]*?\"")

dic = {'og:title': '', 'og:description': '', 'og:image': ''}

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
    return content[0][len("content="):]

def get_iframe_tag(line):
    extracted = p_iframe.findall(line)
    return extracted

def get_src(line):
    srcs = p_src.findall(line)
    if len(srcs) == 0:
        return None
    return srcs[0][len("src="):].replace('\"', '').strip()

def parse_line(line):
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
        #print("item :", item)
        src = get_src(item)
        #print("src :", src)
        if src == None:
            continue
        elif src.startswith("/PostView.naver?"):
            print("download from naver")
            new_url = "https://blog.naver.com" + src
            print("new url :", new_url)
            html = get(new_url)
            print("new content :", html)
            parse(html)

def parse(html):
    if type(html) is str:
        parse_line(html)
    elif type(html) is list:
        for line in html:
            parse_line(line)

    return dic

def get(url):
    with urllib.request.urlopen(url) as response:
        response_str = response.read().decode('utf-8')
        return response_str


if __name__ == '__main__':
    sample_file = open('sample3.html', 'r')
    lines = sample_file.readlines()
    dic = parse(lines)
    print(dic)
#    for key in dic:
#        print(key)