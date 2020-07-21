from django.shortcuts import render, redirect
from . import util
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .helpers import normalize_str
import markdown2

class SearchForm(forms.Form):
    search = forms.CharField(label="search", max_length="25")

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
            search = form.cleaned_data["search"]

            #holds the possible matches for search query
            search_matches = []

            # if search is in current wiki entries
            for page in util.list_entries():
                if page.lower() == search.lower():
                    # return redirect(f"wiki/{page}")
                    # this reverse() func uses the url "name" attribute for redirection
                    return HttpResponseRedirect(reverse("entry", kwargs={"entry": page}))
                else:
                    #if substring of search query matches with wiki entries
                    #add to list
                    if search.lower() in page.lower():
                        search_matches.append(page)

            # else, return the sorted list of possible search results
            return render(request, "encyclopedia/search.html", {
                "search": sorted(search_matches)
            })

        # form is invalid, render errors        
        return render (request, "encyclopedia/search.html", {
            "form": form
        })
    return render(request, "encyclopedia/error.html", {
        "entry": "Please use search on homepage for searching."
    })
