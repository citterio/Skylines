from subprocess import check_call

def pngnq(stdin, stdout):
    check_call(['pngnq'], stdin=stdin, stdout=stdout)
