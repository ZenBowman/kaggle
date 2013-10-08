#!/usr/bin/python

import sys
import nltk

def clean(some_string):
    return some_string.strip().strip('"').strip()

# Function 1 and 2 are both expected to be predicates
def find_discriminator(fn, function1, function2):
    f = open(fn)
    function1Tfunction2F = 0
    function1Tfunction2T = 0
    function1Ffunction2F = 0
    function1Ffunction2T = 0

    for line in f.readlines():
        elems = [clean(x) for x in line.split('\t')]
        
        v1 = function1(elems)
        v2 = function2(elems)
        
        if v1 and v2:
            function1Tfunction2T += 1
        elif v1 and (not v2):
            function1Tfunction2F += 1
        elif (not v1) and v2:
            function1Ffunction2T += 1
        elif (not v1) and (not v2):
            function1Ffunction2F += 1
            
    f.close()

    return (function1Tfunction2F, function1Tfunction2T,
            function1Ffunction2F, function1Ffunction2T)
        
def coerce_int(element):
    try:
        return int(element)
    except:
        return 0

def contains_date(bp):
    i = 2000
    while i < 2020:
        res = str(i)
        if bp.find(res) >= 0:
            return True
        i += 1
    return False

def contains_day(bp):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
            "Saturday", "Sunday"]
    for elem in days:
        if bp.find(elem) >= 0:
            return True
        if bp.find(elem.lower()) >= 0:
            return True
    return False

def contains_news(bp):
    text = nltk.word_tokenize(bp)
    return text.count("news") > 0

def is_news(elems):
    url = elems[0]
    boilerplate = elems[2]
    return (url.find("news") >= 0) or (contains_news(boilerplate))

def is_news_default(elems):
    return coerce_int(elems[17])

def label(elems):
    return coerce_int(elems[26])

def present_results(vals):
    (f1Tf2F, f1Tf2T,f1Ff2F, f1Ff2T) = vals
    f1T = float(f1Tf2F + f1Tf2T)
    f1F = float(f1Ff2F + f1Ff2T)

    print "Number of times f1 was true = %s" % f1T
    print "\tf2 false | f1 true = %s (%s percent)" % (f1Tf2F, f1Tf2F/f1T)
    print "\tf2 true | f1 true = %s (%s percent)" % (f1Tf2T, f1Tf2T/f1T)
        
    print "Number of times f2 was false = %s" % f1F
    print "\tf2 false | f1 false = %s (%s percent)" % (f1Ff2F, f1Ff2F/f1F)
    print "\tf2 true | f1 false = %s (%s percent)" % (f1Ff2T, f1Ff2T/f1F)
        
if __name__ == "__main__":
    vals = find_discriminator(sys.argv[1], is_news, label)
    present_results(vals)
        
