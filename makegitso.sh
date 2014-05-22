#! /bin/bash

##########
# Gisto - Gitso is to support others
# 
# Copyright 2008 - 2010: Aaron Gerber, Derek Buranen
#
# Gitso is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Gitso is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Gitso.  If not, see <http://www.gnu.org/licenses/>.
##########


##
# Helper methods
############################


#
# Creates the source package, works on all UNIX/LINUX based platforms
#
function mksrc {
		P=`pwd`
		TMP_PKG="../pkg"

		# Clean up first.
		find . -name "*~" -exec rm {} ';'

		rm -rf $OSX_BUILD_DIR
		rm -rf $RPM_BUILD_DIR
		rm -rf $DEB_TARGZ_PATH
		rm -rf $P/*.bz2
		rm -rf $P/*.tar
		rm -rf $P/*.gz
		rm -rf $P/*.app
		rm -rf $P/*.dmg
		rm -rf $P/*.deb
		rm -rf $P/*.rpm
		rm -rf $P/*.exe
		rm -rf $TMP_PKG

		# Create the SRC file
		mkdir -p $TMP_PKG/trunk/
		cp -r ./ $TMP_PKG/trunk/
 		find $TMP_PKG/trunk -name ".svn" -exec rm -rf {} 2>&1 > /dev/null ';' 2>&1 > /dev/null
		mv $TMP_PKG/trunk $TMP_PKG/gitso-0.6.2
		tar -cj -C $TMP_PKG/ gitso-0.6.2 > $P/$SRC
		rm -rf $TMP_PKG
}


#
# Create the .app folder for snow leopard, it uses a different version of pythong
# And because py2app needs to know there, we just use different config files.
#
function snowLeopardDMG {
	# Grab the default option and then reset it at the end.
	#defaults write com.apple.versioner.python Prefer-32-Bit -bool yes
	echo -e "Creating Gitso.app "
	rm -f setup.py
	rm -rf $OSX_BUILD_DIR
	
	echo -e ".."
	
	python arch/osx/setup.py py2app
	
	echo -e ".."
	cp arch/osx/Info_OSX-10.6.plist $OSX_BUILD_DIR/Gitso.app/Contents/Info.plist
	
	cp COPYING $OSX_BUILD_DIR/Gitso.app/Contents/Resources/
	cp PythonApplet.icns $OSX_BUILD_DIR/Gitso.app/Contents/Resources/
	
	tar xvfz arch/osx/OSXvnc.tar.gz
	mv OSXvnc $OSX_BUILD_DIR/Gitso.app/Contents/Resources/

	tar xvfz arch/osx/cotvnc.app.tar.gz
	mv cotvnc.app $OSX_BUILD_DIR/Gitso.app/Contents/Resources/
	
	cp icon.ico $OSX_BUILD_DIR/Gitso.app/Contents/Resources/
	cp icon.png $OSX_BUILD_DIR/Gitso.app/Contents/Resources/
	cp __init__.py $OSX_BUILD_DIR/Gitso.app/Contents/Resources/
	cp ArgsParser.py $OSX_BUILD_DIR/Gitso.app/Contents/Resources/
	cp Processes.py $OSX_BUILD_DIR/Gitso.app/Contents/Resources/
	cp ConnectionWindow.py $OSX_BUILD_DIR/Gitso.app/Contents/Resources/
	cp AboutWindow.py $OSX_BUILD_DIR/Gitso.app/Contents/Resources/
	cp GitsoThread.py $OSX_BUILD_DIR/Gitso.app/Contents/Resources/
	cp NATPMP.py $OSX_BUILD_DIR/Gitso.app/Contents/Resources/
	
	cp arch/osx/libjpeg-copyright.txt $OSX_BUILD_DIR/Gitso.app/Contents/Frameworks/
	cp arch/osx/osxnvc_echoware-copyright.txt $OSX_BUILD_DIR/Gitso.app/Contents/Resources/OSXvnc/
	cp arch/osx/cotvnc-copyright.txt $OSX_BUILD_DIR/Gitso.app/Contents/Resources/cotvnc.app/contents/Resources
	cp arch/osx/osxvnc-copyright.txt $OSX_BUILD_DIR/Gitso.app/Contents/Resources/OSXvnc/
	
	echo -e " [done]\n"
	
	echo -e "Creating $DMG_OSX_106"
	rm -f $DMG_OSX_106
	
	mkdir $OSX_BUILD_DIR/Gitso
	cp arch/osx/dmg_DS_Store $OSX_BUILD_DIR/Gitso/.DS_Store
	ln -s /Applications/ $OSX_BUILD_DIR/Gitso/Applications
	
	mv "$OSX_BUILD_DIR/Gitso.app" "$OSX_BUILD_DIR/Gitso/"
	cp -r arch/osx/Readme.rtfd $OSX_BUILD_DIR/Gitso/Readme.rtfd
	
	echo -e "..."
	hdiutil create -srcfolder $OSX_BUILD_DIR/Gitso/ $DMG_OSX_106
	echo -e "... [done]\n"
}


#
# Create the .app folder for Leopard, it uses a different version of pythong
# And because py2app needs to know there, we just use different config files.
#
function LeopardDMG {
	echo -e "Creating Gitso.app "
	rm -f setup.py
	rm -rf $OSX_BUILD_DIR
	
	echo -e ".."
	
	python arch/osx/setup.py py2app
	
	echo -e ".."
	cp arch/osx/Info_OSX-10.5.plist $OSX_BUILD_DIR/Gitso.app/Contents/Info.plist
	
	cp COPYING $OSX_BUILD_DIR/Gitso.app/Contents/Resources/
	cp PythonApplet.icns $OSX_BUILD_DIR/Gitso.app/Contents/Resources/
	
	tar xvfz arch/osx/OSXvnc.tar.gz
	mv OSXvnc $OSX_BUILD_DIR/Gitso.app/Contents/Resources/

	tar xvfz arch/osx/cotvnc.app.tar.gz
	mv cotvnc.app $OSX_BUILD_DIR/Gitso.app/Contents/Resources/
	
	cp icon.ico $OSX_BUILD_DIR/Gitso.app/Contents/Resources/
	cp icon.png $OSX_BUILD_DIR/Gitso.app/Contents/Resources/
	cp __init__.py $OSX_BUILD_DIR/Gitso.app/Contents/Resources/
	cp ArgsParser.py $OSX_BUILD_DIR/Gitso.app/Contents/Resources/
	cp Processes.py $OSX_BUILD_DIR/Gitso.app/Contents/Resources/
	cp ConnectionWindow.py $OSX_BUILD_DIR/Gitso.app/Contents/Resources/
	cp AboutWindow.py $OSX_BUILD_DIR/Gitso.app/Contents/Resources/
	cp GitsoThread.py $OSX_BUILD_DIR/Gitso.app/Contents/Resources/
	cp NATPMP.py $OSX_BUILD_DIR/Gitso.app/Contents/Resources/
	
	cp arch/osx/libjpeg-copyright.txt $OSX_BUILD_DIR/Gitso.app/Contents/Frameworks/
	cp arch/osx/osxnvc_echoware-copyright.txt $OSX_BUILD_DIR/Gitso.app/Contents/Resources/OSXvnc/
	cp arch/osx/cotvnc-copyright.txt $OSX_BUILD_DIR/Gitso.app/Contents/Resources/cotvnc.app/contents/Resources
	cp arch/osx/osxvnc-copyright.txt $OSX_BUILD_DIR/Gitso.app/Contents/Resources/OSXvnc/
	
	echo -e " [done]\n"
	
	echo -e "Creating $DMG_OSX_105"
	rm -f $DMG_OSX_105
	
	mkdir $OSX_BUILD_DIR/Gitso
	cp arch/osx/dmg_DS_Store $OSX_BUILD_DIR/Gitso/.DS_Store
	ln -s /Applications/ $OSX_BUILD_DIR/Gitso/Applications
	
	mv "$OSX_BUILD_DIR/Gitso.app" "$OSX_BUILD_DIR/Gitso/"
	cp -r arch/osx/Readme.rtfd $OSX_BUILD_DIR/Gitso/Readme.rtfd
	
	echo -e "..."
	hdiutil create -srcfolder $OSX_BUILD_DIR/Gitso/ $DMG_OSX_105
	echo -e "... [done]\n"
}


#
# Displays the help menu
#
function helpMenu {
	echo -e "Usage makegitso.sh: [ BUILD OPTIONS ] [ OPTIONS ]"
	echo -e "\tBUILD OPTIONS"
	echo -e "\t--fedora\tMake package for Fedora. (only avaible on Fedora)"
	echo -e "\t--opensuse\tMake package for OpenSUSE. (only avaible on OpenSUSE)"

	# Cent OS doesn't have wxWidget in it's repo....
	#echo -e "\t--centos\tMake package for CentOS. (only avaible on CentOS)"

	echo -e "\t--source\tMake the source package. (All UNIX/Linux systems)\n"
	echo -e "\tOPTIONS:"
	echo -e "\t--no-clean\tDo not remove the build directory."
	echo -e "\t--help  \tThese options."
	exit 0

}


##
# Initialize values
############################
DMG_OSX_106="Gitso_0.6.2_mac_SnowLeopard.dmg"
DMG_OSX_105="Gitso_0.6.2_mac_Leopard.dmg"
DEB="../gitso_0.6.2_all.deb"
TARGZ="../gitso_0.6.2_all.tar.gz"
SRC="gitso_0.6.2_src.tar.bz2"
RPM="gitso-0.6.2-1.i586.rpm"
RPMOUT=""

OSX_BUILD_DIR=`pwd`"/dist"
RPM_BUILD_DIR=`pwd`"/build"
DEB_BUILD_DIR="debian/gitso"
DEB_TARGZ_PATH="gitso"

CLEAN="yes"
RPMNAME=""
USESRC="no"


##
# Get Comman line arguments
############################
for param in "$@"
do
	if test "${param}" = "--no-clean"; then
		CLEAN="no"
	elif test "${param}" = "--fedora"; then
		RPMNAME="fedora"
		RPMOUT="gitso_0.6.2-1_fedora.i386.rpm"
	elif test "${param}" = "--centos"; then
		RPMNAME="centos"
		RPMOUT="gitso_0.6.2-1_centos.i386.rpm"
	elif test "${param}" = "--opensuse"; then
		RPMNAME="opensuse"
		RPMOUT="gitso_0.6.2-1_opensuse.i586.rpm"
	elif test "${param}" = "--source"; then
		USESRC="yes"
	else
		helpMenu
	fi
done


##
# Create packages!
########################
if [ "$USESRC" = "yes" ]; then
	# Creating the source
	echo -n "Creating gitso $SRC...."
	mksrc
	echo -e " [done]\n"

elif [ "`uname -a | grep Darwin`" != "" ]; then
	#We're on OS X
	
	if test `which py2applet`; then
		# To Make cotvnc
		# cvs -z3 -d:pserver:anonymous@cotvnc.cvs.sourceforge.net:/cvsroot/cotvnc co -P cotvnc
		#
		# cd cotvnc
		# patch -p0 < [Gitso-path]/arch/osx/cotvnc-gitso.diff
		#
		# Then in xCode build cotvnc
		# find build/Development/
		# rename Chicken Of The VNC.app to cotvnc.app
		# remove cotvnc.app/Contents/Resources/*non English.lproj
		# rename cotvnc.app/Contents/MacOS/Chicken Of The VNC to cotvnc.app/Contents/MacOS/cotvnc
		# 
		# Patch was made with: diff -aurr . ../cotvnc-gitso/ > cotvnc-gitso.diff
		#
		LeopardDMG
		snowLeopardDMG
	else
		echo -e "Error, you need py2applet to be installed."
	fi
	
elif test "`uname -a 2>&1 | grep Linux | grep -v which`"; then
	#We're on Linux
	
	if test "`which dpkg 2>&1 | grep -v which`"; then
		# Deb version of Gitso.
		echo -n "Creating $DEB"
		dpkg-buildpackage -us -uc -d -b
		echo -e " [done]"
	
		# Standalone version of Gitso.
		echo -n "Creating $TARGZ"
		rm -rf $DEB_TARGZ_PATH
		
		cp -r $DEB_BUILD_DIR $DEB_TARGZ_PATH
		rm -rf $DEB_TARGZ_PATH/DEBIAN
	
		echo -n ".."
		cp arch/linux/README-stand-alone.txt $DEB_TARGZ_PATH/README
		cp arch/linux/run-gitso.sh $DEB_TARGZ_PATH/
		mv $DEB_TARGZ_PATH/usr/bin $DEB_TARGZ_PATH/bin
		mv $DEB_TARGZ_PATH/usr/share $DEB_TARGZ_PATH/share
		rm -rf $DEB_TARGZ_PATH/usr/
		
		echo -n "."
		tar -cvzf $TARGZ $DEB_TARGZ_PATH 2>&1 > /dev/null
		
		echo -e " [done]\n"
		
	elif test "`which rpm 2>&1 | grep -v which`"; then
		# RPM version of Gitso
		if [ "$RPMNAME" = "fedora" ]; then
			SPEC="gitso_rpm_fedora.spec"
			# yum --nogpgcheck install gitso_0.6.2-1_fedora.i386.rpm 
		elif [ "$RPMNAME" = "opensuse" ]; then
			SPEC="gitso_rpm.spec"
		elif [ "$RPMNAME" = "centos" ]; then
			SPEC="gitso_rpm_centos.spec"
		else
		    echo -e "Error: Invalid RPM Type: '$RPMNAME'\n\tPlease specify one of the following:\n\t--opensuse\n\t--fedora\n"
		    exit 1
		fi

		echo "Creating $RPM"
		export RPM_BUILD_DIR=$RPM_BUILD_DIR
		TMP="$RPM_BUILD_DIR/rpm/tmp"
		BUILD_ROOT="$RPM_BUILD_DIR/rpm/tmp/gitso-root"

		# We need this because the rpmbuild below needs to the source ball.
		# Also realize that mksrc is going to clean-up, so if you creat diste files before this line
		# They will be deleted.
		mksrc
		
		mkdir -p $RPM_BUILD_DIR/rpm/{BUILD,RPMS/$ARCH,RPMS/noarch,SOURCES,SRPMS,SPECS,tmp}
		mkdir -p $BUILD_ROOT

		cp $SRC $RPM_BUILD_DIR/rpm/SOURCES/$SRC

		cp arch/linux/$SPEC $TMP
		perl -e 's/%\(echo \$HOME\)/$ENV{'RPM_BUILD_DIR'}/g;' -pi $TMP/$SPEC
		
		if [ "$RPMNAME" = "fedora" ]; then
			rpmbuild -ba $TMP/$SPEC
		elif [ "$RPMNAME" = "opensuse" ]; then
			export RPM_BUILD_ROOT="$HOME/rpmbuild/BUILDROOT/gitso-0.6.2-1.i386"
			rpmbuild -ba --buildroot=$RPM_BUILD_ROOT $TMP/$SPEC
		elif [ "$RPMNAME" = "centos" ]; then
			export RPM_BUILD_ROOT="$HOME/rpmbuild/BUILDROOT/gitso-0.6.2-1.i386"
			rpmbuild -ba --buildroot=$RPM_BUILD_ROOT $TMP/$SPEC
		fi	
		
		find $RPM_BUILD_DIR/rpm/RPMS -name "*.rpm" -exec cp {} $RPMOUT ';'

		echo -e " [done]\n"
	fi

fi

# Clean up
if [ "$CLEAN" = "yes" ]; then
	echo -e "Cleaning up...."
	rm -rf $RPM_BUILD_DIR
	dpkg-buildpackage -tc -us -uc -d -b
	rm -rf $DEB_TARGZ_PATH
	find . -name "*.pyc" -exec rm {} ';'
	echo -e " [done]\n"
fi

