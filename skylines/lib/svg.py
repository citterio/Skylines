from subprocess import check_call

def rsvg_convert(stdin, stdout):
    check_call(['rsvg-convert'], stdin=stdin, stdout=stdout)
