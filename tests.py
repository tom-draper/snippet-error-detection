from validation import *
from js2py.internals.simplex import JsException

def test_valid_javascript():
    x1 = valid_javascript('var x = 0;')
    x2 = valid_javascript('vart x = 0;')
        
    success = (True, None)
    
    assert x1 == success
    assert x2[0] == False