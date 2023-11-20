from django.shortcuts import render

from . import util


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