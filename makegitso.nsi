; makegitso.nsi
; ----------------
; Package Gitso for Windows using NSIS
; 
; Copyright 2008 - 2014: Aaron Gerber and Derek Buranen and AustP
; 
; Gitso is free software: you can redistribute it and/or modify
; it under the terms of the GNU General Public License as published by
; the Free Software Foundation, either version 3 of the License, or
; (at your option) any later version.
; 
; Gitso is distributed in the hope that it will be useful,
; but WITHOUT ANY WARRANTY; without even the implied warranty of
; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
; GNU General Public License for more details.
; 
; You should have received a copy of the GNU General Public License
; along with Gitso.  If not, see <http://www.gnu.org/licenses/>.
;--------------------------------

!define VERSION "0.6.3" 
Name "Gitso ${VERSION}"
Icon "./icon.ico"
UninstallIcon "./icon.ico"
OutFile "gitso-install.exe"

; The default installation directory
InstallDir $PROGRAMFILES\Gitso
; Registry key to check for directory (so if you install again, it will overwrite the old one automatically)
InstallDirRegKey HKLM "Software\Gitso" "Install_Dir"

;--------------------------------
; Version Information
  VIProductVersion "0.6.3.0"
  VIAddVersionKey "ProductName" "Gitso"
  VIAddVersionKey "Comments" "Gitso is to support others"
  VIAddVersionKey "CompanyName" "https://github.com/AustP/Gitso"
  VIAddVersionKey "LegalCopyright" "GPL 3"
  VIAddVersionKey "FileDescription" "Gitso"
  VIAddVersionKey "FileVersion" "${VERSION}"
;--------------------------------

;--------------------------------
; Pages
Page components
Page directory
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles
;--------------------------------

Section "Gitso"
  SectionIn RO
  SetOutPath $INSTDIR
	  ; Write the installation path into the registry
	  ; Write the uninstall keys for Windows
	  WriteRegStr HKLM SOFTWARE\Gitso "Install_Dir" "$INSTDIR"  
	  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Gitso" "DisplayName" "Gitso"
	  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Gitso" "UninstallString" '"$INSTDIR\uninstall.exe"'
	  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Gitso" "NoModify" 1
	  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Gitso" "NoRepair" 1
	  WriteUninstaller "uninstall.exe"
  File ".\hosts.txt"
  File ".\icon.ico"
  File ".\icon.png"
  File ".\COPYING"
  File ".\dist\Gitso.exe"
  File ".\dist\icon.ico"
  File ".\dist\library.zip"
  File ".\dist\msvcp71.dll"
  File ".\dist\MSVCR71.dll"
  File ".\dist\python25.dll"
  File ".\dist\pywintypes25.dll"
  File ".\dist\bz2.pyd"
  File ".\dist\win32api.pyd"
  File ".\dist\_ssl.pyd"
  File ".\dist\_socket.pyd"
  File ".\dist\select.pyd"
  File ".\dist\unicodedata.pyd"
  File ".\dist\w9xpopen.exe"
  File ".\dist\wx._controls_.pyd"
  File ".\dist\wx._core_.pyd"
  File ".\dist\wx._gdi_.pyd"
  File ".\dist\wx._misc_.pyd"
  File ".\dist\wx._windows_.pyd"
  File ".\dist\wxbase28uh_net_vc.dll"
  File ".\dist\wxbase28uh_vc.dll"
  File ".\dist\wxmsw28uh_adv_vc.dll"
  File ".\dist\wxmsw28uh_core_vc.dll"
  File ".\dist\wxmsw28uh_html_vc.dll"
  File ".\arch\win32\tightVNC_LICENCE.txt"
  File ".\arch\win32\tightVNC_COPYING.txt"
  File ".\arch\win32\tightVNC_README.txt"
  File ".\arch\win32\VNCHooks_COPYING.txt"
  File ".\arch\win32\msvcr71_README.txt"
 ;start menu items
  CreateDirectory "$SMPROGRAMS\Gitso"
  CreateShortCut "$SMPROGRAMS\Gitso\Gitso.lnk" "$INSTDIR\Gitso.exe" "" "$INSTDIR\icon.ico" 0
  File ".\arch\win32\vncviewer.exe"
  File ".\arch\win32\WinVNC.exe"
  File ".\arch\win32\VNCHooks.dll"

 ;Registry tweaks to TightVNC's server
  WriteRegDWORD HKCU "Software\ORL\WinVNC3" "RemoveWallpaper" 1
  WriteRegDWORD HKCU "Software\ORL\WinVNC3" "EnableFileTransfers" 1
 ;set default password to something so WinVNC.exe doesn't complain about having no password
  WriteRegBin HKCU "SOFTWARE\ORL\WinVNC3" "Password" "238f16962aeb734e"
  WriteRegBin HKCU "SOFTWARE\ORL\WinVNC3" "PasswordViewOnly" "238f16962aeb734e"
 ;Try to set it for all users, but I'm not positive this works
  WriteRegDWORD HKLM "Software\ORL\WinVNC3" "RemoveWallpaper" 1
  WriteRegDWORD HKLM "Software\ORL\WinVNC3" "EnableFileTransfers" 1
  WriteRegBin HKLM "SOFTWARE\ORL\WinVNC3" "Password" "238f16962aeb734e"
  WriteRegBin HKLM "SOFTWARE\ORL\WinVNC3" "PasswordViewOnly" "b0f0ac1997133bc9"
SectionEnd


; Uninstall
;------------------------------------------------------
Section "Uninstall"
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Gitso"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Gitso"
  ; Remove files and uninstaller
  Delete $INSTDIR\vncviewer.exe
  Delete $INSTDIR\VNCHooks.dll
  Delete $INSTDIR\WinVNC.exe
  ; Remove shortcuts and folder
  RMDir /r "$SMPROGRAMS\Gitso"
  RMDir /r $INSTDIR
SectionEnd
