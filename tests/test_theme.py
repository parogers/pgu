
import tempfile
import pytest
import pygame
import site
site.addsitedir('.')

import pgu
from pgu.gui.theme import Theme

from test_utils import (
    temp_theme,
    temp_legacy_theme,
)


def test_it_loads_default_theme():
    theme = Theme()
    assert theme


def test_it_loads_custom_theme():
    with temp_theme('''
[some-element]
padding = 1
''') as temp_dir:
        theme = Theme(temp_dir)
        assert theme


def test_it_raises_error_if_style_not_found():
    theme = Theme()
    with pytest.raises(pgu.gui.errors.StyleError):
        theme.getstyle('does not exist', '', '')


def test_it_loads_fonts():
    style_ini = '''
[some-element]
font = Vera.ttf 16
'''
    assets = ['Vera.ttf']
    with temp_theme(style_ini, assets) as temp_dir:
        theme = Theme(temp_dir)
        font = theme.getstyle('some-element', '', 'font')
        assert isinstance(font, pygame.font.Font)


def test_it_loads_background_surface():
    style_ini = '''
[some-element]
background = sample.png
'''
    assets = ['sample.png']
    with temp_theme(style_ini, assets) as temp_dir:
        theme = Theme(temp_dir)
        bg = theme.getstyle('some-element', '', 'background')
        assert isinstance(bg, pygame.Surface)


def test_it_loads_pseudo_class_styles():
    style_ini = '''
[some-element:hover]
padding = 1

[some-element:press]
padding = 2
'''
    with temp_theme(style_ini) as temp_dir:
        theme = Theme(temp_dir)
        assert theme.getstyle('some-element', 'hover', 'padding') == 1
        assert theme.getstyle('some-element', 'press', 'padding') == 2


def test_it_loads_multiple_sections():
    style_ini = '''
[some-element]
padding = 1

[another-element]
padding = 2
'''
    with temp_theme(style_ini) as temp_dir:
        theme = Theme(temp_dir)
        assert theme.getstyle('some-element', '', 'padding') == 1
        assert theme.getstyle('another-element', '', 'padding') == 2


def test_it_loads_colors():
    style_ini = '''
[some-element]
color = #123456
'''
    with temp_theme(style_ini) as temp_dir:
        theme = Theme(temp_dir)
        assert theme.getstyle('some-element', '', 'color') == (0x12, 0x34, 0x56)


def test_it_loads_string_values():
    style_ini = '''
[some-element]
label = this-is-some-text
'''
    with temp_theme(style_ini) as temp_dir:
        theme = Theme(temp_dir)
        assert theme.getstyle('some-element', '', 'label') == 'this-is-some-text'


# TODO - is this a bug?
def test_it_loads_only_first_token_of_string():
    style_ini = '''
[some-element]
label = this is some text
'''
    with temp_theme(style_ini) as temp_dir:
        theme = Theme(temp_dir)
        assert theme.getstyle('some-element', '', 'label') == 'this'


def test_it_loads_legacy_config_txt():
    config_txt = '''
element.something padding 1
element:hover background sample.png
'''
    assets = ['sample.png']
    with temp_legacy_theme(config_txt, assets) as temp_dir:
        theme = Theme(temp_dir)
        assert theme.getstyle('element.something', '', 'padding') == 1
        assert isinstance(theme.getstyle('element', 'hover', 'background'), pygame.Surface)


def test_it_raises_error_if_empty_theme_directory():
    with tempfile.TemporaryDirectory() as temp_dir:
        with pytest.raises(IOError, match='Cannot load theme: missing style.ini or config.txt'):
            Theme(temp_dir)
