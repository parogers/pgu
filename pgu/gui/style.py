"""
"""

from . import pguglobals
from .errors import StyleError

class Style(object):
    """The class used by widget for the widget.style

    This object is used mainly as a dictionary, accessed via widget.style.attr,
    as opposed to widget.style['attr'].  It automatically grabs information
    from the theme via value = theme.get(widget.cls,widget.pcls,attr)

    """
    def __init__(self, obj, dict):
        self.obj = obj
        for k,v in dict.items():
            self.__dict__[k]=v

    # Verify that the given style is defined, otherwise raises an StyleError exception. This
    # is used by various widgets to check that they have all required style information.
    def check(self, attr):
        if (not self.exists(attr)):
            desc = self.obj.cls
            if (self.obj.pcls): desc += "."+self.obj.pcls
            raise StyleError("Cannot find the style attribute '%s' for '%s'" % (attr, desc))

    # Checks if the given style attribute exists
    def exists(self, attr):
        try:
            value = pguglobals.app.theme.getstyle(self.obj.cls, self.obj.pcls, attr)
            return True
        except StyleError:
            return False

    def __getattr__(self, attr):
        # Lookup the attribute
        try:
            value = pguglobals.app.theme.getstyle(self.obj.cls, self.obj.pcls, attr)
        except StyleError:
            value = 0

        if attr in (
            'border_top','border_right','border_bottom','border_left',
            'padding_top','padding_right','padding_bottom','padding_left',
            'margin_top','margin_right','margin_bottom','margin_left',
            'align','valign','width','height',
            ): self.__dict__[attr] = value
        return value

    def __setattr__(self, attr, value):
        self.__dict__[attr] = value

