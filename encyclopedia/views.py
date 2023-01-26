from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown
from . import util
import random


def index(request):
    if request.method == "POST":
        title = request.POST.get('q')
        search = util.get_entry(title)
        if search == None:
            similar = []
            for entry in util.list_entries():
                if title.upper() in entry.upper():
                    similar += [entry]
            return render(request, "encyclopedia/index.html", {
                "entries": similar
            })
        else:
            return render(request, "encyclopedia/wiki.html", {
                "title": title,
                "body": markdown.markdown(search)
            })
        
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    return render(request, "encyclopedia/wiki.html", {
        "title": title,
        "body": markdown.markdown(util.get_entry(title))
    })
def new(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if title in util.list_entries():
            return render(request, "encyclopedia/new.html",{
            "message": 'Error: Entry with provided title already exists',
            "entries": util.list_entries()
        })
        else:
            util.save_entry(title, content)
            return render(request, "encyclopedia/wiki.html", {
                "title": title,
                "body": markdown.markdown(util.get_entry(title))
            })

    return render(request, "encyclopedia/new.html",{
        "entries":util.list_entries()
    })

def edit(request, title):
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        return render(request, "encyclopedia/wiki.html", {
            "title": title,
            "body": markdown.markdown(util.get_entry(title))
        })
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content":util.get_entry(title)
    })

def random_entry(request):
    title = random.choice(util.list_entries())
    return render(request, "encyclopedia/wiki.html", {
        "title": title,
        "body": markdown.markdown(util.get_entry(title))
    })