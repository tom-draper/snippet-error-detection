import ast
import json
from html5lib import HTMLParser, html5parser
from xml.etree import ElementTree
import js2py


def valid_python(code: str) -> tuple[bool, SyntaxError]:
    try:
        ast.parse(code)
    except SyntaxError as e:
        return False, e
    return True, None


def valid_json(code: str) -> tuple[bool, ValueError]:
    try:
        json.loads(code)
    except ValueError as e:
        return False, e
    return True, None


def valid_html(code: str) -> tuple[bool, html5parser.ParseError]:
    try:
        parser = HTMLParser(strict=True)
        parser.parseFragment(code)
    except html5parser.ParseError as e:
        return False, e
    return True, None


def valid_xml(code: str) -> tuple[bool, ElementTree.ParseError]:
    try:
        ElementTree.fromstring(code)
    except ElementTree.ParseError as e:
        return False, e
    return True, None


def valid_javascript(code: str) -> tuple[bool, js2py.internals.simplex.JsException]:
    try:
        esprima = js2py.require("esprima@4.0.1")
        esprima.parse(code)
    except js2py.internals.simplex.JsException as e:
        return False, e
    return True, None

