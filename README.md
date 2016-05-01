# What is this?
This is a client for the service [PushBullet](https://www.pushbullet.com/) intended for GNOME and other XDG compatible desktops. This was originally inspired by [this project](https://github.com/erinaceous/gtk-pushbullet). While I would have rather just contributed to that project, I figured I would be able to get a lot more done if I started a project that was compatible license-wise with [pyPushBullet](https://github.com/Azelphur/pyPushBullet).
It should be noted that as of right now this is mostly a proof of concept, although I hope to have more functionality added soon.

# Requirements
- PyGObject
- [pyPushBullet](https://github.com/Azelphur/pyPushBullet)

# How to launch
First you need to setup your API key. Right now we don't have any option to do this from the program itself, so you have to write your own config file. Simply place a file that looks like this in `~/.config/gtk-pushbullet.conf`:
```
[main]
api_key = o.TlesCPUmApqYTxIMVkpWei5Yof7SYgSp
```

Then run the client using
```
./src/client.py
```

Eventually this will be much easier, and you'll have the ability to install this through pip.
