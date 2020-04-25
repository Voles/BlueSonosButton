import daemon
import logging

from controlSonos import do_main_program

formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler("./output.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

with daemon.DaemonContext(files_preserve = [handler.stream]):
    do_main_program(logger)
