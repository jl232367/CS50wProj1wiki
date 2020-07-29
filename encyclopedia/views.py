from django.shortcuts import render, redirect
from . import util
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .helpers import normalize_str
from markdown2 import Markdown
import markdown2

class SearchForm(forms.Form):
    search = forms.CharField(label="search", max_length="25")

class CreatePageForm(forms.Form):
    title = forms.CharField(label="Title", max_length="50")
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": 10, "cols": 50}))

class EditPageForm(forms.Form):
    content = forms.CharField(help_text="Some Text here", widget=forms.Textarea(attrs={"rows": 10, "cols": 50}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    # if entry matches a page
    md = Markdown()
    entry_list = util.list_entries()
    for page in entry_list:
        # check ignores case
        if page.lower() == entry.lower():

            # gets page from entries and converts md to html
            converted_page = md.convert(util.get_entry(page))

            return render(request, "encyclopedia/entry.html", {
                "entry": converted_page
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
                    # SIMPLEST: return redirect(f"wiki/{page}")
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


def create(request):
    # ensures that form action is POST, and initiates processing of data
    if request.method == "POST":
        form = CreatePageForm(request.POST)

        # checks that new input is valid
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            
            # check if the entry already exists
            for page in util.list_entries():
                # if so, then present error page
                if page.lower() == title.lower():
                    return render(request, "encyclopedia/error.html", {
                        "entry": f"{title} was already a wiki page. Try again next time!",
                    })

            # otherwise, save new page and redirect to new page
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", kwargs={"entry": title}))

    return render(request, "encyclopedia/create.html", {
        "form": CreatePageForm()
    })    


def edit(request):


    return render(request, "encyclopedia/edit.html", {
        "form": EditPageForm(initial=request.GET)
    })