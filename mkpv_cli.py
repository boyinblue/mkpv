#!/usr/bin/env python3

# Make preview
def make_preview():
    url = input("URL : ")

    import url_preview

    html = url_preview.get_text_from_url(url)
    if html == None:
        messagebox.showinfo("Unable to load URL", url)
        return 255

    dic = url_preview.parse(html.split('\n'))

    print("\n")
    print("=================================================")
    print(" Output")
    print("=================================================")
    print("{{% assign preview_image_url = '{}' %}}".format(dic['og:image']))
    print("{{% assign preview_url = '{}' %}}".format(url))
    print("{{% assign preview_title = '{}' %}}".format(dic['og:title']))
    print("{{% assign preview_description = '{}' %}}".format(dic['og:description']))
    print("{% include body-preview.html %}")
    print("=================================================")

make_preview()
