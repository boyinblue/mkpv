#!/usr/bin/env python3

import urllib.request
import re

p_meta = re.compile("<meta .* />")
p_property = re.compile("property=\"[^\"]*\" ")
p_content = re.compile("content=\"[^\"]*\"")

dic = {'og:title': '', 'og:description': '', 'og:image': ''}

def get_meta_tag(line):
    extracted = p_meta.findall(line)
    if len( extracted ) == 0:
        return None
    return extracted[0]

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

def parse_line(line):
    print("Line :", line)
    extracted = get_meta_tag(line)
    if extracted == None:
        return
    property = get_property(line)
    content = get_content(line)
    if property != None:
        print("property : ", property)
        print("content : ", content)
        dic[property] = content
    if property == "og:title":
        dic['og:title'] = content
        print("og:title :", content)
    elif property == "og:description":
        dic['og:description'] = content
        print("og:description :", content)
    elif property == "og:image":
        dic['og:image'] = content
        print("og:image :", content)

    #            atoms = item.split(' ')
    #            for atom in atoms:
    #                print(atom)

def parse(html):
    if type(html) is str:
        parse_line(html)
    elif type(html) is list:
        for line in html:
            parse_line(line)

    return dic

def get(url):
    with urllib.request.urlopen(url) as response:
        return response.read().decode('utf-8')


if __name__ == '__main__':
    sample_file = open('sample.html', 'r')
    lines = sample_file.readlines()
    dic = parse(lines)
    print(dic)
#    for key in dic:
#        print(key)