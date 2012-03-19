"""
"""

from . import pguglobals
from .errors import StyleError

class Style(object):
    """Widget style information. If the style attribute is not explicitly defined in the
    style, the fallback is to use the default defined by the global theme. Example:

    Arguments:
        widget -- The widget this style applies to
        values -- A dictionary of style information to use instead of the theme defaults

    Example:
        # Create a button
        w = Button("Testing")

        # Print out the default value for 'padding_left'
        print w.style.padding_left

        # Change the default style for all buttons
        app.theme.putstyle("button", "", "padding_left", 10)
        print w.style.padding_left

        # Define 'padding_left' only for this widget
        w.style.padding_left = 1
        # Alternate syntax
        w.style["padding_left"] = 2

    """
    def __init__(self, widget, values):
        self.widget = widget
        for (key, value) in values.items():
            setattr(self, key, value)

    # Verify that the given style is defined, otherwise raises an StyleError exception. This
    # is used by various widgets to check that they have all required style information.
    def check(self, attr):
        if (not self.exists(attr)):
            desc = self.widget.cls
            if (self.widget.pcls): desc += "."+self.widget.pcls
            raise StyleError("Cannot find the style attribute '%s' for '%s'" % (attr, desc))

    # Checks if the given style attribute exists
    def exists(self, attr):
        try:
            self.getstyle(attr)
            return True
        except StyleError:
            return False

    def getstyle(self, attr):
#        if (attr == "font"):
#            print "getstyle", self.widget, self.widget.name

        if (hasattr(self.widget, "name") and self.widget.name):
            try:
                return pguglobals.app.theme.getstyle(self.widget.cls+"#"+self.widget.name, self.widget.pcls, attr)
            except StyleError:
                pass
        #print "fallback", self.widget.cls, self.widget.pcls, attr
        return pguglobals.app.theme.getstyle(self.widget.cls, self.widget.pcls, attr)

    def __getattr__(self, attr):
        # Lookup the attribute
        try:
            value = self.getstyle(attr)
        except StyleError:
            value = 0

#        if attr in (
#            'border_top','border_right','border_bottom','border_left',
#            'padding_top','padding_right','padding_bottom','padding_left',
#            'margin_top','margin_right','margin_bottom','margin_left',
#            'align','valign','width','height',
#            ): self.__dict__[attr] = value
        return value

#    def __setattr__(self, attr, value):
#        self.__dict__[attr] = value


