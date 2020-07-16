from django.shortcuts import render
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    # if entry doesn't exist
    entry_list = util.list_entries()
    if entry not in entry_list:
        return render(request, "encyclopedia/error.html", {
            "entry": entry
        })
    # else, return entry page
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "text": util.get_entry(entry)
    })