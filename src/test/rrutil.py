import pexpect, signal, sys, time

__all__ = [ 'expect_gdb', 'send_gdb','expect_rr', 'send_rr',
            'interrupt_gdb', 'ok' ]

# Public API
def expect_gdb(what):
    expect(gdb_rr, what)

def expect_rr(what):
    expect(gdb_rr, what)

def interrupt_gdb():
    try:
        gdb_rr.kill(signal.SIGINT)
    except Exception, e:
        failed('interrupting gdb', e)
    expect_gdb('stopped.')

def send_gdb(what):
    send(gdb_rr, what)

def send_rr(what):
    send(gdb_rr, what)

def ok():
    clean_up()

# Internal helpers
TIMEOUT_SEC = 20
# gdb and rr are part of the same process tree, so they share
# stdin/stdout.
gdb_rr = None

def clean_up():
    global gdb_rr
    if gdb_rr:
        gdb_rr.close(force=1)
        gdb_rr = None

def expect(prog, what):
    try:
        prog.expect(what)
    except Exception, e:
        failed('expecting "%s"'% (what), e)

def failed(why, e):
    print 'FAILED:', why
    if e:
        print 'exception:', e
    clean_up()
    sys.exit(1)

def get_exe():
    '''Return the image to be debugged'''
    return sys.argv[1]

def get_rr_cmd():
    '''Return the command that should be used to invoke rr, as the tuple
  (executable, array-of-args)'''
    rrargs = sys.argv[2:]
    return (rrargs[0], rrargs[1:])

def send(prog, what):
    try:
        prog.send(what)
    except Exception, e:
        failed('sending "%s"'% (what), e)

def set_up():
    global gdb_rr
    try:
        gdb_rr = pexpect.spawn(*get_rr_cmd(), timeout=TIMEOUT_SEC, logfile=open('rr.log', 'w'))
        expect_gdb(r'\(gdb\)')
    except Exception, e:
        failed('initializing rr and gdb', e)

set_up()
