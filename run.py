import daemon

from controlSonos import do_main_program

with daemon.DaemonContext():
    do_main_program()
