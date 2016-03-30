### Switch emacs input language by ctrl+shift or alt+shift

This script allows you to switch emacs input languages (`toggle-input-language`)
by `ctrl+shift` or `alt+shift` keybindings in linux.

### Dependencies

 * xorg-xinput
 * [xkb-switch](https://github.com/ierton/xkb-switch)
 * python3

### Installation
 * Download [this script](emacs-switch-lang.py) and make it executable
 * Install `xorg-xinput` packages using your package manager
 * Install [xkb-switch](https://github.com/ierton/xkb-switch)
 * Add keybinding into your *~/.emacs* file:
``` emacs-lisp
 (global-set-key (kbd "<f13>") 'toggle-input-method)
 (add-hook 'minibuffer-setup-hook
            (lambda ()
              (local-set-key (kbd "<f13>") 'toggle-input-method)))
```

### Usage

```
emacs-switch-lang.py [-h] [--bind {ctrl+shift,alt+shift}]
                          [--switch-back-cmd SWITCH_BACK_CMD]
                          [--key-send-cmd KEY_SEND_CMD] [-v]

Send a signal (key) to emacs when ctrl+shift or alt+shift is pressed.

optional arguments:
  -h, --help            show this help message and exit
  --bind {ctrl+shift,alt+shift}
                        keybinding for swithing-language
  --switch-back-cmd SWITCH_BACK_CMD
                        command to switch language back to default language
  --key-send-cmd KEY_SEND_CMD
                        command to send signal to emacs
  -v, --verbose         Verbose output for debugging
```

Simply add this script to autostart with preferred *--bind* option: `ctrl+shift` or `alt+shift`.

#### Example

``` shell
./emacs-switch-lang.py --bind ctrl+shift
```

### How it works

It runs in background and listens for key presses. Whenever
`ctrl+shift`/`alt+shift` are pressed, it checks active window is Emacs and if it
is the case it sends *<f13>* key to it and switches language back to us-english.
Emacs sees *<f13>* key and toggle input method.

### Known issues

 * This version wont work in case emacs running in command line

### Credits

As prototype I took script by https://github.com/grandchild/autohidewibox
