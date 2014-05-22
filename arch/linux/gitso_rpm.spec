
%define _topdir      		%(echo $HOME)/rpm
%define _tmppath        %{_topdir}/tmp
%define _prefix         /usr/share
%define _defaultdocdir  %{_prefix}/doc
%define _mandir         %{_prefix}/man
%define buildroot				%{_tmppath}/gitso-root


Name:				gitso
Summary:		Gitso - Is to Support Others
Version:		0.6.3
Release:		1
License:		GPL 3
Group:			Internet 
URL:				https://github.com/AustP/Gitso

Requires:		python, x11vnc, tightvnc, wxGTK, python-wxGTK
Buildroot:	%{_tmppath}/gitso-root
Packager:  	Aaron Gerber



%description
Gitso is a frontend to reverse VNC connections. It is meant to be a 
simple two-step process that connects one person to another's screen.

%prep
%setup

%build

%install
./arch/linux/build_rpm.sh %(echo $HOME)

%clean

%files
/usr/bin/gitso

%{_prefix}/applications/gitso.desktop

%{_prefix}/doc/gitso/COPYING
%{_prefix}/doc/gitso/README
%{_prefix}/doc/gitso/changelog.gz

%{_prefix}/gitso/Gitso.py
%{_prefix}/gitso/ConnectionWindow.py
%{_prefix}/gitso/AboutWindow.py
%{_prefix}/gitso/GitsoThread.py
%{_prefix}/gitso/Processes.py
%{_prefix}/gitso/ArgsParser.py
%{_prefix}/gitso/__init__.py
%{_prefix}/gitso/hosts.txt
%{_prefix}/gitso/NATPMP.py
%{_prefix}/gitso/icon.ico
%{_prefix}/gitso/icon.png

%{_mandir}/man1/gitso.1.gz

%changelog 
* Sun Oct 26 2008 Aaron Gerber <gerberad@gmail.com>
- Created RPM
