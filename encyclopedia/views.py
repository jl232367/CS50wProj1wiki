from django.shortcuts import render
from . import util
from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label="query", max_length="50")



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def normalize_str(word):
    first_letter = word[0].upper()
    return first_letter + word[1:]

def entry(request, entry):
    # if entry doesn't exist
    entry_list = util.list_entries()
    if normalize_str(entry) not in entry_list:
        return render(request, "encyclopedia/error.html", {
            "entry": entry
        })
    # else, return entry page
    return render(request, "encyclopedia/entry.html", {
        "entry": normalize_str(entry),
        "text": util.get_entry(entry)
    })

def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            return render(request, "encyclopedia/entry.html", {
                "entry": util.get_entry(form.query)
            })
