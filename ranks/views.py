from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from .models import Preference

names = ["Brandon Quinlan", "Brian Scaramella", "David Kahn", \
    "David Udelson", "Jeremy Miller", "Matthew Weidman", "Niranjan Ravi"]

nums = list(range(1, 11))

def index(request):
    ctx = {"names": names, "nums": nums, "submitted": False}
    return render(request, 'ranks/index.html', ctx)

def submit(request):
    user = request.POST['user']

    wtotal = 0.
    for name in names:
        wtotal += float(request.POST[name])

    for name in names:
        w = float(request.POST[name]) / wtotal
        p = user + " " + name
        pref = Preference(prefid=p, user=user, choice=name, weight=w)
        print(pref.user)
        pref.save()
    
    ctx = {"submitted": True}
    return render(request, 'ranks/index.html', ctx)

def get_3C7():
    """
    List of all possible combinations of 3 choose 7
    Each combination is list of 1s and 0s
    1s are in the group of 3, 0s are in the group of 4
    """
    combos = []
    n = 7
    for i in range(0, n-2):
        for j in range(i+1, n-1):
            for k in range(j+1, n):
                c = [0] * n
                c[i] = 1
                c[j] = 1
                c[k] = 1
                combos.append(c)
    return combos

def combo_to_names(c):
    """
    Convert a combination, consisting of 1s and 0s, into
    2 lists of names corresponding to that group
    """
    n1 = []
    n2 = []
    for i in range(len(c)):
        if c[i] == 1:
            n1.append(names[i])
        elif c[i] == 0:
            n2.append(names[i])
    return n1, n2

def combo_to_string(c):
    """
    Convert a combination, consisting of 1s and 0s, into
    2 lists of names written as a string
    """
    n1, n2 = combo_to_names(c)
    s1 = ', '.join(n1)
    s2 = ', '.join(n2)
    return "Group1: [" + s1 + "]; Group 2: [" + s2 + "]"

def group_score(ns):
    """
    Get the total group score of one list of names
    """
    score = 0
    objs = Preference.objects
    for n1 in ns:
        for n2 in ns:
            if n1 != n2:
                filt = objs.filter(user=n1, choice=n2)
                if len(filt) > 0:
                    score += filt[0].weight
    return score

def grouping_score(c):
    """
    Get the score from a combination, consisting of 1s and 0s.
    """
    n1, n2 = combo_to_names(c)
    return group_score(n1) + group_score(n2)

def argmax(l):
    """
    Finds the index of the largest element in a list
    """
    besti = 0
    for i in range(len(l)):
        if l[besti] < l[i]:
            besti = i
    return besti

def results(request):
    prefs = Preference.objects.all()
    users = set()
    for pref in prefs:
        users.add(pref.user)
    numusers = len(users)

    combos = get_3C7()
    groupings = [combo_to_string(c) for c in combos]
    scores = [int(grouping_score(c) * 1000)/1000 for c in combos]
    g = (sorted(zip(scores, groupings))[::-1])[:3]

    ctx = {"users": numusers, "groupings": g}
    return render(request, 'ranks/results.html', ctx)