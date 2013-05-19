#!/usr/bin/env python

"""
A set of classes for validating data:

  read from text files (or other source)
 
  in GUI dialogs:
     wxPython So far, but could be anything

"""


def Property(func):
    """ nifty property decorator I found on the net"""
    return property(**func())


class ValidatedData(object):
    """
    The base class for a validated data type
    
    all it needs in an is_valid property
    """
    def __init__(self, string=""):
        self.string = string

    @Property
    def invalid():
        doc = """
        invalid property
        
        returns False if the value is valid

        returns an error message if the value is invalid
         
         common use:
        
        if not this.invalid:
            do_something
        else:
            do_something with the error message(this.invalid) 
        
        The "double negative" 
        """
        
        def fget(self):
            return False
        return locals()
        
    @Property
    def value():
        def fget(self):
            return self.string
        return locals()
        


class ValidatedFloat(ValidatedData):

    def __init__(self, string="", minimum=float("-inf"), maximum=float("inf")):
        self.string = string
        self.minimum = minimum
        self.maximum = maximum

    @Property
    def invalid():
        def fget(self):
            try:
                f = float(self.string)
                if f > self.maximum:
                    return "value larger than %f"%self.maximum
                elif f < self.minimum:
                    return "value smaller than %f"%self.minumum
                return False
            except ValueError:
                return "not a valid floating point number"
        return locals()
                
    @Property
    def value():
        def fget(self):
            if not self.invalid:
                return float(self.string)
            else:
                raise ValueError("The value: %s is valid")
        return locals()

    def set(self, string):
        self.string = string
        return self.value


class junk(object):
    val = 0
    @Property
    def prop():
        doc = "this is the doc string"
        def fget(self):
            print getting
            return 3+4+self.val
        def fset(self, val):
            print "setting:", val
            self.val = val
        def fdel(self):
            del self._value
        return locals()
            
if __name__ == "__main__":
    j = junk
    
    j.prop = 4
    print j.prop
    j.prop = 6
    print j.prop
    
