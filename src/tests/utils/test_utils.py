from re import Pattern

from utils import create_valid_extension_pattern_from


def test_create_valid_extension_pattern_from():
    p = create_valid_extension_pattern_from()
    assert type(p) is Pattern
    assert p.pattern == '/*(.jpg|.jpeg|.JPG|.JPEG|.jpe|.jfif|.pjpeg|.pjp|.png|.gif|.tiff|.tif|.webp|.svg|.svgz)$'
