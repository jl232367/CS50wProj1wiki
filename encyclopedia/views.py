from django.shortcuts import render
from . import util
from django import forms
from django.http import HttpResponse

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

def normalize_str(word):
    first_letter = word[0].upper()
    return first_letter + word[1:]

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
    # return HttpResponse("Success")

    if request.method == "POST":

        form = SearchForm(request.POST)


        if form.is_valid():
            search = form.cleaned_data["search"]
            return render(request, "encyclopedia/search.html", {
                "search": search
            })

            return HttpResponse("Success")    

        #render errors        
        return render (request, "encyclopedia/search.html", {
            "form": form
        })
            
            # entry_list = util.list_entries()

            # if form.data in entry_list:

            #     return render(request, "encyclopedia/search.html", {
            #         "entry": form,
            #     })

    
    # if request.method == "POST":
    #     form = SearchForm(request.POST)
    #     if form.is_valid():
    #         return render(request, "encyclopedia/entry.html", {
    #             "entry": util.get_entry(form),
    #             "text": util.get_entry(query)
    #         })
