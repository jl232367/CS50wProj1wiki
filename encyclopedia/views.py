from django.shortcuts import render
from . import util
from django import forms
from django.http import HttpResponse
from .helpers import normalize_str


class SearchForm(forms.Form):
    search = forms.CharField(label="q", max_length="25")

    # for validating data
    # def clean(self):
    #     cleaned_data = super().clean()
    #     search = cleaned_data.get("search")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# def normalize_str(word):
#     first_letter = word[0].upper()
#     return first_letter + word[1:]


def entry(request, entry):
    # if entry matches a page
    entry_list = util.list_entries()
    for page in entry_list:
        # check ignores case
        if page.lower() == entry.lower():
            return render(request, "encyclopedia/entry.html", {
                "entry": normalize_str(entry),
                "text": util.get_entry(entry)
            })
    # else, page doesn't exist, return error
    return render(request, "encyclopedia/error.html", {
        "entry": entry
    })


def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["q"]

            # if search is in current wiki entries
            for page in util.list_entries():
                if page.lower() == search.lower():
                    return render(request, "encyclopedia/entry.html", {
                        "entry": normalize_str(search),
                        "text": util.get_entry(search)
                    })

            # else, return the list of possible search results
            return render(request, "encyclopedia/search.html", {
                "search": search
            })

        # form is invalid, render errors        
        return render (request, "encyclopedia/search.html", {
            "form": form
        })
    return render(request, "encyclopedia/error.html", {
        "entry": "Please use search on homepage for searching."
    })
