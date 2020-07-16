from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    # if entry doesn't exist
    # if 

    # else, return entry page

    return render(request, "encyclopedia/entry.html", {
        "title": title
    })