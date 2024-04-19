
!include "MUI2.nsh"
!include "WinMessages.nsh"
!include "LogicLib.nsh"

# Mui metadata
!define MUI_ICON "app.ico"
!define MUI_UNICON "${MUI_ICON}"
!define MUI_ABORTWARNING
!define MUI_HEADERIMAGE
!define LOGO_ICON_FILE "${MUI_ICON}"

# App metadata
!define APPNAME "Paperback Self-Diagnosis Tool"
Name "${APPNAME}"
Icon "${MUI_ICON}"
# Define the installer name and output directory
InstallDir "$DOCUMENTS\Ivanmatthew Programs\PaperbackSelfDiagnosisTool"
Outfile "paperback-selfdiagnosis-tool-setup.exe"

RequestExecutionLevel user

Function .onInstSuccess
    Exec "explorer $INSTDIR"
FunctionEnd
; Function RESTRICT_DIR_PAGE
;     !if "${MUI_SYSVERSION}" >= 2.0
;         SendMessage $mui.DirectoryPage.Directory ${EM_SETREADONLY} 1 0
;         EnableWindow $mui.DirectoryPage.BrowseButton 0
;     !else
;         FindWindow $0 '#32770' '' $HWNDPARENT
;         GetDlgItem $1 $0 0x3FB
;         SendMessage $1 ${EM_SETREADONLY} 1 0
;         GetDlgItem $1 $0 0x3E9
;         EnableWindow $1 0
;     !endif
; FunctionEnd

# Set the default section
!insertmacro MUI_PAGE_WELCOME
; !define MUI_PAGE_CUSTOMFUNCTION_SHOW RESTRICT_DIR_PAGE
; !insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_INSTFILES

!define MUI_FINISHPAGE_TITLE "Installation Complete"
!define MUI_FINISHPAGE_TEXT "The ${APPNAME} has been successfully installed on your computer, at $INSTDIR."
!define MUI_FINISHPAGE_RUN "$INSTDIR\${APPNAME}.exe"
!insertmacro MUI_PAGE_FINISH
Section
    # Set the installation directory
    SetOutPath $INSTDIR

    WriteUninstaller "$INSTDIR\uninstall.exe"

    # Copy the files from the pyinstaller dist directory
    File "dist\${APPNAME}\*"
    SetOutPath "$INSTDIR\_internal"
    File /nonfatal /a /r "dist\${APPNAME}\_internal\"

    # Create the start menu shortcut
    CreateShortCut "$SMPROGRAMS\${APPNAME}.lnk" "$INSTDIR\${APPNAME}.exe"
    CreateShortCut "$SMPROGRAMS\Uninstall ${APPNAME}.lnk" "$INSTDIR\uninstall.exe"
SectionEnd

# Define the uninstaller
UninstallIcon "${MUI_ICON}"
UninstallText "Uninstall the ${APPNAME} from your computer."
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH
Section "Uninstall"
    StrCpy $1 "${APPNAME}.exe"
    nsProcess::_FindProcess "$1"
    Pop $0
    ${If} $0 == 0
        MessageBox MB_ICONEXCLAMATION|MB_OK "Please close ${APPNAME} before uninstalling."
        Abort
    ${Else}
        Delete "$SMPROGRAMS\${APPNAME}.lnk"
        Delete "$SMPROGRAMS\Uninstall ${APPNAME}.lnk"
        RMDir /r "$INSTDIR"
    ${EndIf}
SectionEnd
!insertmacro MUI_LANGUAGE "English"