#define MyAppName "RGS Quotation Generator"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "RYHAN GLOBAL SOLUTIONS"
#define MyAppExeName "RGS Quotation Generator.exe"

[Setup]
AppId={{8A5C6D8D-7C45-4F67-9C42-RGS-QUOTATION-001}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={autopf}\RGS Quotation Generator
DefaultGroupName=RGS Quotation Generator

OutputDir=installer
OutputBaseFilename=RGS Quotation Generator Setup

Compression=lzma
SolidCompression=yes

SetupIconFile=assets\RGS_Logo.ico

ArchitecturesInstallIn64BitMode=x64compatible
DisableProgramGroupPage=yes

[Files]
Source: "dist\RGS Quotation Generator\*"; \
    DestDir: "{app}"; \
    Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autodesktop}\RGS Quotation Generator"; \
    Filename: "{app}\RGS Quotation Generator.exe"; \
    WorkingDir: "{app}"

Name: "{group}\RGS Quotation Generator"; \
    Filename: "{app}\RGS Quotation Generator.exe"; \
    WorkingDir: "{app}"

[Run]
Filename: "{app}\RGS Quotation Generator.exe"; \
    Description: "Launch RGS Quotation Generator"; \
    Flags: nowait postinstall skipifsilent