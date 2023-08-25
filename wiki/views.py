from django.shortcuts import render
import markdown
from . import util
import random


def index(request):
    return render(request, "wiki/index.html", {
        "entries": util.list_entries()
    })

def convert_to_HTML(entry_name):
    md = markdown.Markdown()
    entry  = util.get_entry(entry_name)
    html = md.convert(entry) if entry else None
    return html

def entry(request, entry_name):
    html = convert_to_HTML(entry_name)
    if html is None:
        return render(request, "wiki/wrong_entry.html", {
            "entryTitle": entry_name
    })
    else:
        return render(request, "wiki/entry.html", {
            "entry": html,
            "entryTitle": entry_name
        })


def search(request):

    if request.method == 'POST':

        input = request.POST['q']
        html = convert_to_HTML(input)

        entries = util.list_entries()
        if input in entries:
            return render(request, "wiki/entry.html", {
                "entry": html,
                "entryTitle": input
            })
        else:
            search_pages = []
            for entry in entries:
                if input in entry:
                    search_pages.append(entry)
            return render(request, "wiki/search.html", {
                "entries": search_pages,
            })

def new(request):
      return render(request, "wiki/new.html")

def save(request):
    if request.method == 'POST':
    
        input_title = request.POST['title']
        input_text = request.POST['text']
        entries = util.list_entries()
        if input_title in entries:
            return render(request, "wiki/already_exist.html")
        else:
            util.save_entry(input_title, input_text)
            html = convert_to_HTML(input_title)
            return render(request, "wiki/entry.html", {
                "entry": html,
                "entryTitle": input_title
            })

def rand(request):
    arr = util.list_entries()
    entry_title = random.choice(arr)
    html = convert_to_HTML(entry_title)
    return render(request, "wiki/entry.html", {
            "entry": html,
            "entryTitle": entry_title
        })

            
def edit(request):
    if request.method == 'POST':
        input_title = request.POST['title']
        text = util.get_entry(input_title)
        return render(request, "wiki/edit.html", {
            "entry": text,
            "entryTitle": input_title
        })

def save_edit(request):
    if request.method == 'POST':
        input_title = request.POST['title']
        input_text = request.POST['text']
        util.save_entry(input_title, input_text)
        html = convert_to_HTML(input_title)
        return render(request, "wiki/entry.html", {
            "entry": html,
            "entryTitle": input_title
        })