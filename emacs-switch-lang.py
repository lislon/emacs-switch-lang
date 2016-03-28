#!/usr/bin/python3

# Dependencies:
# * xkb-switch https://github.com/ierton/xkb-switch
# * xorg-xinput

# Put in your ~/.emacs config:
#  (global-set-key (kbd "<f13>") 'toggle-input-method)

import re
import os.path as path
import sys
import subprocess
import argparse

# Left, Right keys codes
ctrl_keys = ["37", "105"]
shift_keys = ["50", "52"]
alt_keys = ["64", "108"]

cmd_switch_to_us = "xkb-switch -s us"
cmd_key_send = "xdotool key F13"
emacs_wm_class = "Emacs"
verbose = False


def parse_arguments():
           parser = argparse.ArgumentParser(
               description='Send a signal (key) to emacs when ctrl+shift or alt+shift is pressed.')

           parser.add_argument("--bind", help="keybinding for switch language",
                               choices=["ctrl+shift", "alt+shift"],
                               default="alt+shift")
           parser.add_argument("--switch-back-cmd",
                               help="command to switch language back to default language",
                               default=cmd_switch_to_us)
           parser.add_argument("--key-send-cmd", help="command to send signal to emacs",
                               default=cmd_key_send)
           parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")

           return parser.parse_args()

def debug(msg):
    if verbose:
        print(msg)

def get_active_window_class():
    root = subprocess.Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE)

    for line in root.stdout:
        l = line.decode("utf-8").strip()
        m = re.search('^_NET_ACTIVE_WINDOW.* ([\w]+)$', l)
        if m != None:
            id_ = m.group(1)
            id_w = subprocess.Popen(['xprop', '-id', id_, 'WM_CLASS'], stdout=subprocess.PIPE)
            break

    if id_w != None:
        for line in id_w.stdout:
            l = line.decode("utf-8").strip()
            match = re.match("WM_CLASS\(\w+\) = \"(.+)\", \"(?P<name>.+)\"$", l)
            if match != None:
                return {"id": id_, "wmclass": match.group("name") }

    return {"id": None, "wmclass": None }

def send_signal_to_emacs():
    if get_active_window_class()['wmclass'] == emacs_wm_class:
        # Send a key to active window
        subprocess.call(cmd_switch_to_us.split(' ', 2))
        # Switch language back to us-english
        subprocess.call(cmd_key_send.split(' ', 2))
        debug("Switch lang.")

try:
    args = parse_arguments()

    first_keys = shift_keys
    if (args.bind == "ctrl+shift"):
        second_keys = ctrl_keys
    else:
        second_keys = alt_keys

    cmd_switch_to_us = args.switch_back_cmd
    cmd_key_send = args.key_send_cmd
    verbose = args.verbose
    print("Start listening to {}".format(args.bind))

    proc = subprocess.Popen(['xinput', '--test-xi2', '--root', '3'], stdout=subprocess.PIPE)

    field = None
    keystate = None

    first_pressed = False
    second_pressed = False

    for line in proc.stdout:
        l = line.decode("utf-8").strip()
        eventmatch = re.match("EVENT type (\\d+) \\(.+\\)", l)
        detailmatch = re.match("detail: (\\d+)", l)

        if eventmatch:
            # debug(eventmatch)
            try:
                field = "event"
                keystate = eventmatch.group(1)
            except IndexError:
                field = None
                keystate = None

        if (field is "event") and detailmatch:
            debug(detailmatch)

            try:
                if detailmatch.group(1) in first_keys:
                    if keystate == "13":  # press
                        debug("Ctrl pressed")
                        first_pressed = True
                    if keystate == "14":  # release
                        debug("Ctrl released")
                        if first_pressed and second_pressed:
                            send_signal_to_emacs()
                        first_pressed = False
                elif detailmatch.group(1) in second_keys:
                    if keystate == "13":  # press
                        debug("Shift pressed")
                        second_pressed = True
                    if keystate == "14":  # release
                        debug("Shift released")
                        if first_pressed and second_pressed:
                            send_signal_to_emacs()
                        second_pressed = False
                else:
                    if first_pressed and second_pressed:
                        debug("Reset state")
                        # Some other keys pressed while ctrl and shift pressed - reset state
                        second_pressed = first_pressed = False

            except IndexError:
                debug("Couldn't parse keystate number.")
                pass
            finally:
                field = None
                keystate = None

except KeyboardInterrupt:
    pass
finally:
    debug("Shutting down")
