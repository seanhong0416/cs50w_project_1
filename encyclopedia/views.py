from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util
from .forms import PageForm, EditForm

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "title":title,
        "content": util.get_entry(title),
    })

def search(request):
    if request.method == 'POST':
        keyword = request.POST["keyword"]
    else:
        keyword = ""
    
    if util.get_entry(keyword) is not None:
        return render(request, "encyclopedia/entry.html", {
            "title":keyword,
            "content":util.get_entry(keyword),
        })
    else:
        entries_match_keyword = []
        for entry in util.list_entries():
            if keyword in entry:
                entries_match_keyword.append(entry)
        return render(request, "encyclopedia/search.html", {
            "keyword":keyword,
            "entries":entries_match_keyword,
        })
    
def add(request):
    error_message = ""

    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) is not None:
                #case where the page that the user wants to add already exists
                error_message = "Page Already Exists!"
                return render(request, "encyclopedia/add.html",{
                    "form":form,
                    "error_message":error_message,
                })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"title":title}))

    else:
        return render(request, "encyclopedia/add.html",{
                    "form":PageForm(),
                    "error_message":error_message,
                })

def edit(request, entry):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid:
            content = form.cleaned_data["content"]
            util.save_entry(entry, content)
            return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"title":entry}))
    else:
        return render(request, "encyclopedia/edit.html",{
            "form":EditForm(),
            "entry":entry,
        })