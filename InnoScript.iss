; Zeb Photo App Installer Script

#define MyAppName "ZebPhotoApp"
#define MyAppVersion "1.5"
#define MyAppPublisher "Muhammad Awais"
#define MyAppExeName "app.exe"

#define MyAppAssocName MyAppName + " File"
#define MyAppAssocExt1 ".png"
#define MyAppAssocExt2 ".jpeg"
#define MyAppAssocExt3 ".jpg"

[Setup]
AppId={{7076022A-B3F0-46EB-8318-58653FB6762C}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\Zeb Photo App
UninstallDisplayIcon={app}\{#MyAppExeName}
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
ChangesAssociations=yes
DisableProgramGroupPage=yes
LicenseFile=G:\Zeb-Photo-App\license.txt
InfoBeforeFile=G:\Zeb-Photo-App\info.txt
InfoAfterFile=G:\Zeb-Photo-App\infoafter.txt
OutputDir=G:\Zeb-Photo-App
OutputBaseFilename=ZebPhotoAppSetup
SetupIconFile=src\icon.ico
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "G:\Zeb-Photo-App\dist\app\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Registry]
; .png
Root: HKCR; Subkey: "{#MyAppAssocExt1}\OpenWithProgids"; ValueType: string; ValueName: "{#MyAppAssocName}"; ValueData: ""; Flags: uninsdeletevalue
Root: HKCR; Subkey: "{#MyAppAssocName}{#MyAppAssocExt1}"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocName}"; Flags: uninsdeletekey
Root: HKCR; Subkey: "{#MyAppAssocName}{#MyAppAssocExt1}\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName},0"
Root: HKCR; Subkey: "{#MyAppAssocName}{#MyAppAssocExt1}\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""

; .jpeg
Root: HKCR; Subkey: "{#MyAppAssocExt2}\OpenWithProgids"; ValueType: string; ValueName: "{#MyAppAssocName}"; ValueData: ""; Flags: uninsdeletevalue
Root: HKCR; Subkey: "{#MyAppAssocName}{#MyAppAssocExt2}"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocName}"; Flags: uninsdeletekey
Root: HKCR; Subkey: "{#MyAppAssocName}{#MyAppAssocExt2}\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName},0"
Root: HKCR; Subkey: "{#MyAppAssocName}{#MyAppAssocExt2}\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""

; .jpg
Root: HKCR; Subkey: "{#MyAppAssocExt3}\OpenWithProgids"; ValueType: string; ValueName: "{#MyAppAssocName}"; ValueData: ""; Flags: uninsdeletevalue
Root: HKCR; Subkey: "{#MyAppAssocName}{#MyAppAssocExt3}"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocName}"; Flags: uninsdeletekey
Root: HKCR; Subkey: "{#MyAppAssocName}{#MyAppAssocExt3}\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName},0"
Root: HKCR; Subkey: "{#MyAppAssocName}{#MyAppAssocExt3}\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
