#define AppName "Latencia"
#define AppVersion "0.1.0"
#define AppPublisher "0xaltair"
#define AppExeName "Latencia.exe"

[Setup]
AppId={{8AECE26C-E8B8-4FFB-A73D-0D0CC5375F53}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={autopf}\Latencia
DefaultGroupName=Latencia
DisableProgramGroupPage=yes
OutputDir=..\release
OutputBaseFilename=Latencia-Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\{#AppExeName}
SetupLogging=yes

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\dist\Latencia.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\Latencia"; Filename: "{app}\Latencia.exe"
Name: "{autodesktop}\Latencia"; Filename: "{app}\Latencia.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\Latencia.exe"; Description: "{cm:LaunchProgram,Latencia}"; Flags: nowait postinstall skipifsilent
