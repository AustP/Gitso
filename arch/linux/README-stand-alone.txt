Gitso is to support others.

We created Gitso as a frontend to reverse VNC connections. It is meant
to be a simple two-step process that connects one person to another's
screen. First, the support person offers to give support. Second, the
person who needs help connects and has their screen remotely visible.
Because Gitso is cross-platform (Ubuntu, OS X and Windows) and uses a
reverse VNC connection, it greatly simplifies the process of getting support.

Gitso 0.6.3: (May 22, 2014)

  * Updated --listen command line to accept port (defaults to 5500)
	* Minimizing now minimizes to tray
	* If --listen is given at start, Gitso will start minimized

Gitso 0.6: (Feb 21, 2010)

  * Complete rewrite of process management.
  * Actually stop VNC Processes (Windows)
  * Support loading remote hosts file.
  * Command line switches
  *     --dev
  *     --listen
  *     --connect IP
  *     --list list_file
  *     --version
  *     --help
  * manpage for (All UNIX sytems)
  * Support for .rpms (Fedora, OpenSUSE, CentOS)
  * Implement Native VNC listener (OS X)
  * Better process management, user gets notified if connection is broken.
  * Licensing Updates (across the board).
  * Improved documentation. 

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Gitso Distro-independent Code.

Note: If you run Ubuntu, it'd be easier to use gitso_0.6_all.deb. However,
if you aren't running Ubuntu proceed.

Requirements:
	x11vnc
	vncviewer
	wxPython

Usage: ./run-gitso.sh [options]
	Options:
       --listen
       --connect IP
       --list list_file
       --version
       --help


