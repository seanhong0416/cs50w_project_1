import random
import re

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util
from .forms import PageForm, EditForm

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "testing": '<h1>hello<h1>',
    })

def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "title":title,
        "content": markdown_html_conversion(util.get_entry(title)),
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
        print("request method is post")
        form = EditForm(request.POST)
        if form.is_valid():
            print("form is valid")
            content = form.cleaned_data["content"]
            util.save_entry(entry, content)
            return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"title":entry}))
    else:
        print("method is get")
        content = util.get_entry(entry)
        return render(request, "encyclopedia/edit.html",{
            "form":EditForm(initial={'content':content}),
            "entry":entry,
        })

def random_page(request):
    entries = util.list_entries()
    random_pick = random.randrange(0, len(entries))
    entry = entries[random_pick]
    return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"title":entry}))

def markdown_html_conversion(content):
    html_content = content

    #links
    p = re.compile('\[ ( .*? ) \] [ ]* \( ( .*? ) \)' , re.VERBOSE)
    html_content = p.sub(r'<a href="\2">\1</a>', html_content)

    #the headings has to be this order so that the smaller headings can be replaced
    #h3
    p = re.compile('\#\#\# [ ]+ ( .*? ) [\r\n]', re.VERBOSE)
    html_content = p.sub(r'<h3>\1</h3>', html_content)

    #h2
    p = re.compile('\#\# [ ]+ ( .*? ) [\r\n]', re.VERBOSE)
    html_content = p.sub(r'<h2>\1</h2>', html_content)

    #h1
    p = re.compile('\# [ ]+ ( .*? ) [\r\n]', re.VERBOSE)
    html_content = p.sub(r'<h1>\1</h1>', html_content)

    #bold text
    p = re.compile('\*\* ( .*? ) \*\*', re.VERBOSE)
    html_content = p.sub(r'<b>\1</b>', html_content)

    #unordered list items
    p = re.compile('\* [ ]+ ( .*? ) [\r\n]', re.VERBOSE)
    html_content = p.sub(r'<li>\1</li>', html_content)

    #unordered list
    p = re.compile('<li> (.*) </li> [\r\n]', re.VERBOSE)
    html_content = p.sub(r'<ul><li>\1</li></ul>', html_content)

    return html_content