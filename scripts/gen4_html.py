# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from settings_statmart import *
import unittest

TEST = unittest.TestCase()

# <codecell>

def tag(tag, html, attributes=[]):
    attribute_str = "";
    space = ""
    for (name, value) in attributes:
        attribute_str = attribute_str + space + name + "='" + value + "'";
        space = " "
    attribute_str = space + attribute_str
    return "<" + tag + attribute_str + ">" + html + "</" + tag + ">"

def html(html, attributes=[]):
    doctype = "<!DOCTYPE html>\n"
    return doctype + tag("html", html, attributes)

def head(html, attributes=[]):
    return tag("head", html, attributes)

def meta(attributes=[]):
    attribute_str = "";
    space = ""
    for (name, value) in attributes:
        attribute_str = attribute_str + space + name + "='" + value + "'";
        space = " "
    return "<meta " + attribute_str + "/>"

def title(html, attributes=[]):
    return tag("title", html, attributes)

def style(html, attributes=[]):
    return tag("style", html, attributes)

def body(html, attributes=[]):
    return tag("body", html, attributes)

def div(html, attributes=[]):
    return tag("div", html, attributes)

def script(js):
    cdata = "//<![CDATA[\n"
    cdataend = "\n//]]>"
    return tag("script", cdata + js + cdataend, [("type","text/javascript")])

def script_ext(path):
    return "<script type='text/javascript' src='%s'></script>" % (path)

def php_include(filepath):
    return "<?php include('%s'); ?>" % (filepath) #this is providing the full path
    
TEST.assertEqual(body("hello", [("foo","bar"),("woo","war")]),"<body foo='bar' woo='war'>hello</body>")

# <codecell>


                    


# <codecell>


