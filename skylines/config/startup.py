from paste.reloader import watch_file
from skylines.lib.svg import rsvg_convert
from skylines.lib.png import pngnq
from distutils.dep_util import newer

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
    pngpath = 'skylines/public/images/glider_symbol.png'
    png8path = 'skylines/public/images/glider_symbol_msie.png'

    watch_file(svgpath)
    convert_svg(svgpath, pngpath)
    convert_png(pngpath, png8path)
