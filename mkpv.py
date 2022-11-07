#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk, messagebox

# Make Main Window
root = Tk()
root.title("Make Preview From URL")
root.geometry("1000x650")
root.resizable(False, False)

# Make Text Box
url_label = Label(root, text="URL")
url_label.grid(column=0, row=0)
url_str = "https://boyinblue.github.io"
url_textbox = ttk.Entry(root, width=100, textvariable=url_str)
url_textbox.grid(column=1, row=0)
url_textbox.focus()
url_textbox.insert(END, url_str)


# Make preview Button
def make_preview():
    url = url_textbox.get()
#    messagebox.showinfo("Make Preview", url)

    import url_preview

    html = url_preview.get(url)
    raw_textbox.delete(1.0, END)
    raw_textbox.insert(END, html)

    dic = url_preview.parse(html.split('\n'))

    title_textbox.delete(1.0, END)
    title_textbox.insert(END, dic['og:title'])

    desc_textbox.delete(1.0, END)
    desc_textbox.insert(END, dic['og:description'])

    image_textbox.delete(1.0, END)
    image_textbox.insert(END, dic['og:image'])

    dic_textbox.delete(1.0, END)
    dic_textbox.insert(END, dic)

    preview_textbox.delete(1.0, END)
    preview_textbox.insert(END, "{{% assign preview_image_url = '{}' %}}\n".format(dic['og:image']))
    preview_textbox.insert(END, "{{% assign preview_url = '{}' %}}\n".format(url))
    preview_textbox.insert(END, "{{% assign preview_title = '{}' %}}\n".format(dic['og:title']))
    preview_textbox.insert(END, "{{% assign preview_description = '{}' %}}\n".format(dic['og:description']))
    preview_textbox.insert(END, "{{% include body-preview.html %}}\n")

ok_btn = ttk.Button(root, text="Make", width=10, command=make_preview)
ok_btn.grid(column=3, row=0)

# Make Raw Data Text Box
raw_label = Label(root, text = "Raw")
raw_label.grid(column=0, row=2)
raw_textbox = Text(root, width=100, height=10)
raw_textbox.grid(column=1, row=2)

# Parsed Data
title_label = Label(root, text = "og:title")
title_label.grid(column=0, row=3)
title_textbox = Text(root, width=100, height=1)
title_textbox.grid(column=1, row=3)
title_textbox.delete(1.0, END)

image_label = Label(root, text = "og:image")
image_label.grid(column=0, row=4)
image_textbox = Text(root, width=100, height=1)
image_textbox.grid(column=1, row=4)
image_textbox.delete(1.0, END)

desc_label = Label(root, text = "og:description")
desc_label.grid(column=0, row=5)
desc_textbox = Text(root, width=100, height=1)
desc_textbox.grid(column=1, row=5)
desc_textbox.delete(1.0, END)

# Dictionary
dic_label = Label(root, text = "Dictionary")
dic_label.grid(column=0, row=6)
dic_textbox = Text(root, width=100, height=10)
dic_textbox.grid(column=1, row=6)

# Make Result Text Box

preview_label = Label(root, text="Preview")
preview_label.grid(column=0, row=7)
preview_textbox = Text(root, width=100, height=10)
preview_textbox.grid(column=1, row=7)

root.mainloop()
