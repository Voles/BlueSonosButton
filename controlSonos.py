#!/usr/bin/env python
import urllib2
import sys
import os
import json
import evdev
import logging
import time

# Modify your variable here
roomname = "Living" # roomname your Sonos Speaker is located
buttonname = "Satechi Media Button Consumer Control" # also tested with "BT-005"
host = "localhost" # when installed on the same host use localhost
port = "5005" #default 5005
key2commandPairs = {"KEY_PLAYPAUSE":"playpause",
                    "KEY_NEXTSONG":"next",
                    "KEY_PREVIOUSSONG":"previous",
                    "KEY_VOLUMEUP":"groupVolume/+1",
                    "KEY_VOLUMEDOWN":"groupVolume/-1"}
# ---------------------------------------------------------------------

def exit_program():
    try:
        sys.exit(1)
    except SystemExit:
        os._exit(0)


def evaluateResponse(response):
    result = u'\u2717'.encode('utf8')
    j = json.loads(response)

    if j["status"] == "success":
        result = u'\u2713'.encode('utf8')
    return result

def do_main_program(logger):
    logger.info("Script started. Searching for " + buttonname + "...")
    try:
        while True:
                devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
                if len(devices) == 0:
                    logger.debug("No devices found, try running with sudo")
                    time.sleep(5)

                for device in devices:
                    if device.name == buttonname:
                        logger.info("Button found: " + str(device))
                        url = "http://" + host + ":" + port + "/"+ roomname
                        try:
                            device.grab()
                            for event in device.read_loop():
                                if event.type == evdev.ecodes.EV_KEY:
                                     data = evdev.categorize(event)  # Save the event temporarily to introspect it
                                     if data.keystate == 1:  # Down events only
                                        if data.keycode in key2commandPairs:
                                            logger.info("Received event " + data.keycode + " -> Sending command " + key2commandPairs[data.keycode])

                                            try:
                                                response = urllib2.urlopen(url + "/" + key2commandPairs[data.keycode]).read()
                                                logger.debug(evaluateResponse(response))
                                            except Exception, e:
                                                logger.error("Sonos HTTP API: %s", e)
                                        else:
                                            logger.info("You Pressed the " + data.keycode + " key!")
                        except Exception, e:
                            logger.error("Unexpected: %s", e)
                            pass
                    else:
                        pass
    except KeyboardInterrupt:
        logger.debug('Exited')
        exit_program()

if __name__ == "__main__":
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    do_main_program(logger)
