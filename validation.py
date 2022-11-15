import ast
import json
from html5lib import HTMLParser, html5parser
from xml.etree import ElementTree
import js2py


def valid_python(code: str) -> bool:
    try:
        ast.parse(code)
    except SyntaxError:
        return False
    return True


def valid_json(code: str) -> bool:
    try:
        json.loads(code)
    except ValueError:
        return False
    return True


def valid_html(code: str) -> bool:
    try:
        parser = HTMLParser(strict=True)
        parser.parseFragment(code)
    except html5parser.ParseError:
        return False
    return True


def valid_xml(code: str) -> bool:
    try:
        ElementTree.fromstring(code)
    except ElementTree.ParseError:
        return False
    return True


def valid_javascript(code: str) -> bool:
    try:
        esprima = js2py.require("esprima@4.0.1")
        esprima.parse(code)
    except js2py.internals.simplex.JsException:
        return False
    return True

