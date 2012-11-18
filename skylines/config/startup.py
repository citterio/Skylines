from paste.reloader import watch_file
from skylines.lib.svg import rsvg_convert
from skylines.lib.png import pngnq
from distutils.dep_util import newer

def color_svg(svgpath, colorsvgpath, original_color, replacement_color):
    if not newer(svgpath, colorsvgpath): return
    with open(svgpath) as svgfile, open(colorsvgpath, 'w') as colorsvgfile:
        content = svgfile.read()
        content = content.replace(original_color, replacement_color)
        colorsvgfile.write(content)

def convert_svg(svgpath, pngpath):
    if not newer(svgpath, pngpath): return
    with open(svgpath) as svgfile, open(pngpath, 'w') as pngfile:
        rsvg_convert(svgfile, pngfile)

def convert_png(pngpath, png8path):
    if not newer(pngpath, png8path): return
    with open(pngpath) as pngfile, open(png8path, 'w') as png8file:
        pngnq(pngfile, png8file)

def convert_glider_symbols():
    svgpath = 'assets/graphics/glider_symbol.svg'

    watch_file(svgpath)

    for color in ['#004bbd', '#bf0099', '#cf7c00', '#ff0000', '#00c994', '#ffff00']:
        colorsvgpath = 'skylines/public/images/glider_symbol_{}.svg'.format(color[1:])
        pngpath = 'skylines/public/images/glider_symbol_{}.png'.format(color[1:])
        png8path = 'skylines/public/images/glider_symbol_msie_{}.png'.format(color[1:])

        color_svg(svgpath, colorsvgpath, '#ff0000', color)
        convert_svg(colorsvgpath, pngpath)
        convert_png(pngpath, png8path)
