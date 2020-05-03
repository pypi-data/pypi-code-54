#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build XML data in CMI format
"""

from lxml import etree


TEI_NS = "http://www.tei-c.org/ns/1.0"
RNG_SCHEMA = "https://raw.githubusercontent.com/TEI-Correspondence-SIG/" + \
    "CMIF/master/schema/cmi-customization.rng"
PI_TEXT = "href=\""+RNG_SCHEMA+"\" type=\"application/xml\" schematypens" + \
    "=\"http://relaxng.org/ns/structure/1.0\""


def pi_rng():
    """
    create xml model processing instruction
    """
    return etree.ProcessingInstruction("xml-model", PI_TEXT)


def tei_root(children=None):
    """
    create TEI root element <TEI> with (optional) children
    """
    root = etree.Element("TEI")
    root.set("xmlns", TEI_NS)
    add_children(root, children)
    return root


def tei_header(children=None):
    """
    create TEI element <teiHeader> with (optional) children
    """
    header = etree.Element("teiHeader")
    add_children(header, children)
    return header


def tei_file_desc(children=None):
    """
    create TEI element <fileDesc> with (optional) children
    """
    file_desc = etree.Element("fileDesc")
    add_children(file_desc, children)
    return file_desc


def tei_title_stmt(children=None):
    """
    create TEI element <titleStmt> with (optional) children
    """
    title_stmt = etree.Element("titleStmt")
    add_children(title_stmt, children)
    return title_stmt


def tei_title(elem_text):
    """
    crate TEI element <title> with given element text
    """
    title = etree.Element("title")
    title.text = elem_text
    return title


def tei_editor(elem_text):
    """
    create TEI element <editor> with given element text
    """
    editor = etree.Element("editor")
    editor.text = elem_text
    return editor


def tei_email(elem_text):
    """
    create TEI element <email> with given element text
    """
    email = etree.Element("email")
    email.text = elem_text
    return email


def tei_publication_stmt(children=None):
    """
    create TEI element <publicationStmt> with (optional) children
    """
    publication_stmt = etree.Element("publicationStmt")
    add_children(publication_stmt, children)
    return publication_stmt


def tei_publisher(child_ref=None):
    """
    create TEI element <publisher> with (optional) child element <ref>
    """
    publisher = etree.Element("publisher")
    add_child(publisher, child_ref)
    return publisher


def tei_ref(elem_text, attrib_target):
    """
    create TEI element <ref> with @target
    """
    ref = etree.Element("ref")
    ref.set("target", attrib_target)
    ref.text = elem_text
    return ref


def tei_idno(elem_text, attrib_type="url"):
    """
    create TEI element <idno> with @type
    """
    idno = etree.Element("idno")
    idno.set('type', attrib_type)
    idno.text = elem_text
    return idno


def tei_availability(child_license=None):
    """
    create TEI element <availability> with (optional) child element <license>
    """
    availability = etree.Element("availability")
    add_child(availability, child_license)
    return availability


def tei_license(elem_text="", attrib_target=""):
    """
    create TEI element <license> with (optional) text and @target
    """
    if elem_text == "" and attrib_target == "":
        elem_text = "This file is licensed under the terms" \
                        + " of the Creative-Commons-License CC-BY 4.0"
        attrib_target = "https://creativecommons.org/licenses/by/4.0/"
    license = etree.Element("license")
    license.set("target", attrib_target)
    license.text = elem_text
    return license


def tei_source_desc(children=None):
    """
    create TEI element <sourceDesc>
    """
    source_desc = etree.Element("sourceDesc")
    add_children(source_desc, children)
    return source_desc


def tei_bibl(elem_text, attrib_type):
    """
    create TEI element <bibl> with given text and @type
    """
    bibl = etree.Element("bibl")
    bibl.set("type", attrib_type)
    bibl.text = elem_text
    return bibl


def tei_profile_desc(children=None):
    """
    create TEI element <profileDesc>
    """
    profile_desc = etree.Element("profileDesc")
    add_children(profile_desc, children)
    return profile_desc


def tei_corresp_desc(attrib_ref="", children=None):
    """
    create TEI <correspDesc> element with @ref
    """
    corresp_desc = etree.Element("correspDesc")
    if attrib_ref != "":
        corresp_desc.set("ref", attrib_ref)
    add_children(corresp_desc, children)
    return corresp_desc


def tei_corresp_action(attrib_type, children=None):
    """
    create TEI <correspAction> element with @type
    """
    corresp_action = etree.Element("correspAction")
    corresp_action.set("type", attrib_type)
    add_children(corresp_action, children)
    return corresp_action


def tei_date(attrib_when="", attrib_from="", attrib_to=""):
    """
    create TEI <date> element with @when or @from and @to
    """
    date = etree.Element("date")
    if attrib_when != "":
        date.set("when", attrib_when)
    elif attrib_from != "" and attrib_to != "":
        date.set("from", attrib_from)
        date.set("to", attrib_to)
    return date


def tei_place_name(elem_text, attrib_ref=""):
    """
    create TEI <placeName> element with given element text and @ref
    """
    place_name = etree.Element("placeName")
    place_name.text = elem_text
    place_name.set("ref", attrib_ref)
    return place_name


def tei_pers_name(elem_text, attrib_ref=""):
    """
    create TEI <persName> element with given element text and @ref
    """
    pers_name = etree.Element("persName")
    pers_name.text = elem_text
    pers_name.set("ref", attrib_ref)
    return pers_name


def tei_text_empty():
    """
    create TEI element <text> with child elements <body> and <p> (empty)
    """
    text = tei_text()
    body = tei_body()
    body.append(tei_p())
    text.append(body)
    return text


def tei_text():
    """
    create TEI element <text> with child elements <body> and <p> (empty)
    """
    return etree.Element("text")


def tei_body():
    """
    create TEI element <body>
    """
    return etree.Element("body")


def tei_p():
    """
    create TEI element <p>
    """
    return etree.Element("p")


def add_pi(tree):
    """
    add xml-model processing instruction to given element tree
    """
    tree.getroot().addprevious(pi_rng())


def add_child(parent, element):
    """
    add element to parent if element is not None
    """
    if element is not None:
        parent.append(element)


def add_children(parent, elements):
    """
    add elements to parent if elements is not None
    """
    if elements is not None:
        for child in elements:
            parent.append(child)


def pretty(elements):
    """
    pretty print given elements
    """
    print(etree.tostring(elements, pretty_print=True).decode().strip())


def tostr(element):
    """
    convert given element to str
    """
    return etree.tostring(element).decode().strip()
