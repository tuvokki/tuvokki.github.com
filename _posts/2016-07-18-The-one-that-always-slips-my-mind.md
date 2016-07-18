---
layout: post
title: "The one that always slips"
published: true
---
### The one that always slips my mind

You know that feeling, it's something you did, you know what you did but you can't really remember how to fix it. You also know that, right? I have that with a locked terminal when using the command line...

All unix terminals have a feature from way back when a [terminal](http://en.wikipedia.org/wiki/Teleprinter) was a piece of hardware connected to the computer via a serial port. The terminal could send [flow control](http://en.wikipedia.org/wiki/Flow_control#Transmit_flow_control) commands to the computer: [“XON”](http://en.wikipedia.org/wiki/XON/XOFF) (meaning “stop sending me stuff, I'm not ready”) and [“XOFF”](http://en.wikipedia.org/wiki/XON/XOFF) (meaning “ok, throw me what you've got”). I normally recommend turning these features off in your terminal configuration (the command is [`stty -ixon`](http://en.wikipedia.org/wiki/Stty)), but in this particular case, they're useful: press <kbd>Ctrl</kbd>+<kbd>S</kbd> to stop scrolling, and <kbd>Ctrl</kbd>+<kbd>Q</kbd> to resume.

Now, this will be happening again. But at least it will not take me to google again. The above explanation is copied from [stackexchange](http://unix.stackexchange.com/questions/13404/how-do-i-kill-1-gnome-terminal-window/13408#13408).
