#!/usr/bin/env python3

# Make preview
def make_preview():
    url = input("URL : ")
    dic = {'url': url}

    import url_preview

    html = url_preview.get_text_from_url(url)
    if html == None:
        print("Unable to load URL :", url)
        return 255

    url_preview.parse(html.split('\n'), dic)
    preview = url_preview.make_preview(dic)

    print("\n")
    print("=================================================")
    print(" Output")
    print("=================================================")
    print(preview)
    print("=================================================")

make_preview()
