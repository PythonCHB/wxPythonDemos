#!/usr/bin/env python

"""
test_validated_data

tests of the validated_data classes

designed to be run by py.test

"""

import validated_data as vd

def test_init():
    v = vd.ValidatedData()
    assert v.string == ""
    
def test_init2():
    v = vd.ValidatedData("a string")

    assert v.string == "a string"

    assert not v.invalid

## FloatValidator
    
def test_init_():
    v = vd.ValidatedFloat()
    assert v.string == ""
    
def test_float_unbounded():
    v = vd.ValidatedFloat("32.5")
    
    assert not v.invalid
    
    assert v.value == 32.5
    
def test_float_too_big():
    v = vd.ValidatedFloat("32.5", minimum=0.0, maximum=100.0)
    
    assert not v.invalid
    
    assert v.value == 32.5
    
    v.string = "110.0"
    assert v.invalid
    
    

    
    
    
    
