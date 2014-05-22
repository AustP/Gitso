#! /bin/bash

# Check parameters
if test "$1" = ""; then
	echo -e "************************\nError: No arguments were given to build_rpm.sh\n************************\n"
	exit 1
fi

echo -e "Setting up RPM build-root!\n\t"

BUILD_ROOT="$HOME/rpmbuild/BUILDROOT/gitso-0.6.3-1.i386"

mkdir -p $BUILD_ROOT/usr/bin/
mkdir -p $BUILD_ROOT/usr/share/gitso/
mkdir -p $BUILD_ROOT/usr/share/applications/
mkdir -p $BUILD_ROOT/usr/share/doc/gitso/
mkdir -p $BUILD_ROOT/usr/share/man/man1

cp arch/linux/gitso $BUILD_ROOT/usr/bin/

chmod 755 $BUILD_ROOT/usr/bin/gitso
cp arch/linux/gitso.desktop $BUILD_ROOT/usr/share/applications/

cp COPYING $BUILD_ROOT/usr/share/doc/gitso/
cp arch/linux/README.txt $BUILD_ROOT/usr/share/doc/gitso/README
gzip -cf arch/linux/changelog > $BUILD_ROOT/usr/share/doc/gitso/changelog.gz

cp Gitso.py $BUILD_ROOT/usr/share/gitso/
cp ConnectionWindow.py $BUILD_ROOT/usr/share/gitso/
cp AboutWindow.py $BUILD_ROOT/usr/share/gitso/
cp GitsoThread.py $BUILD_ROOT/usr/share/gitso/
cp Processes.py $BUILD_ROOT/usr/share/gitso/
cp ArgsParser.py $BUILD_ROOT/usr/share/gitso/
cp __init__.py $BUILD_ROOT/usr/share/gitso/
cp NATPMP.py $BUILD_ROOT/usr/share/gitso/
cp hosts.txt $BUILD_ROOT/usr/share/gitso/
cp icon.ico $BUILD_ROOT/usr/share/gitso/
cp icon.png $BUILD_ROOT/usr/share/gitso/

gzip -cf arch/linux/gitso.1 > $BUILD_ROOT/usr/share/man/man1/gitso.1.gz

echo 'Done';

