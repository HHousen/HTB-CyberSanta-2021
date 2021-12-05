# Honeypot (300)

## Problem

> Santa really encourages people to be at his good list but sometimes he is a bit naughty himself. He is using a Windows 7 honeypot to capture any suspicious action. Since he is not a forensics expert, can you help him identify any indications of compromise?

1. Find the full URL used to download the malware.
2. Find the malicious's process ID.
3. Find the attackers IP

Flag Format: HTB{echo -n "http://url.com/path.foo_PID_127.0.0.1" | md5sum}
Download Link: http://46.101.25.140/forensics_honeypot.zip

* [forensics_honeypot.zip](http://46.101.25.140/forensics_honeypot.zip)

## Solution

1. This is a memory dump of a computer. We can use [volatility](https://www.volatilityfoundation.org/) to read this memory dump and extra the 3 pieces of information necessary to create the flag. It is of a Windows 7 computer according to the challenge description, but I determined the profile with `./volatility_2.5_linux_x64 -f honeypot.raw kdbgscan`:

    ```
    Volatility Foundation Volatility Framework 2.5
    **************************************************
    Instantiating KDBG using: /home/hhousen/Downloads/volatility_2.5.linux.standalone/honeypot.raw WinXPSP2x86 (5.1.0 32bit)
    Offset (P)                    : 0x2930c68
    KDBG owner tag check          : True
    Profile suggestion (KDBGHeader): Win7SP1x86
    Version64                     : 0x2930c40 (Major: 15, Minor: 7601)
    PsActiveProcessHead           : 0x829494f0
    PsLoadedModuleList            : 0x82950e30
    KernelBase                    : 0x82805000

    **************************************************
    Instantiating KDBG using: /home/hhousen/Downloads/volatility_2.5.linux.standalone/honeypot.raw WinXPSP2x86 (5.1.0 32bit)
    Offset (P)                    : 0x2930c68
    KDBG owner tag check          : True
    Profile suggestion (KDBGHeader): Win7SP0x86
    Version64                     : 0x2930c40 (Major: 15, Minor: 7601)
    PsActiveProcessHead           : 0x829494f0
    PsLoadedModuleList            : 0x82950e30
    KernelBase                    : 0x82805000
    ```

    As you can see, we should use the `Win7SP0x86` or `Win7SP1x86` profile. I wnet with `Win7SP1x86`, but I don't think it matters.

2. We can find the malicious's process ID using the `pslist` command like so: `./volatility_2.5_linux_x64 -f honeypot.raw --profile=Win7SP1x86 pslist`:

    ```
    Volatility Foundation Volatility Framework 2.5
    Offset(V)  Name                    PID   PPID   Thds     Hnds   Sess  Wow64 Start                          Exit                          
    ---------- -------------------- ------ ------ ------ -------- ------ ------ ------------------------------ ------------------------------
    0x8413a940 System                    4      0     76      549 ------      0 2021-11-26 05:12:15 UTC+0000                                 
    0x84fe9c80 smss.exe                236      4      2       32 ------      0 2021-11-26 05:12:15 UTC+0000                                 
    0x84f9bd28 csrss.exe               308    300      9      435      0      0 2021-11-26 05:12:16 UTC+0000                                 
    0x850ba3f0 wininit.exe             348    300      3       75      0      0 2021-11-26 05:12:16 UTC+0000                                 
    0x859f4398 csrss.exe               360    340      7      159      1      0 2021-11-26 05:12:16 UTC+0000                                 
    0x856f5620 services.exe            400    348      8      225      0      0 2021-11-26 05:12:16 UTC+0000                                 
    0x85702590 lsass.exe               408    348      7      615      0      0 2021-11-26 05:12:16 UTC+0000                                 
    0x856fbd28 lsm.exe                 416    348     10      171      0      0 2021-11-26 05:12:16 UTC+0000                                 
    0x85147d28 winlogon.exe            496    340      4      111      1      0 2021-11-26 05:12:17 UTC+0000                                 
    0x858326b8 svchost.exe             572    400     11      368      0      0 2021-11-26 05:12:17 UTC+0000                                 
    0x85899390 VBoxService.ex          636    400     14      123      0      0 2021-11-26 05:12:17 UTC+0000                                 
    0x924cd3a8 svchost.exe             692    400      7      268      0      0 2021-11-25 19:12:18 UTC+0000                                 
    0x85819700 svchost.exe             744    400     17      353      0      0 2021-11-25 19:12:18 UTC+0000                                 
    0x858ed9d8 svchost.exe             848    400     21      464      0      0 2021-11-25 19:12:19 UTC+0000                                 
    0x858f8548 svchost.exe             888    400     41      902      0      0 2021-11-25 19:12:19 UTC+0000                                 
    0x85921030 svchost.exe            1012    400     17      331      0      0 2021-11-25 19:12:19 UTC+0000                                 
    0x8593c260 svchost.exe            1084    400     16      396      0      0 2021-11-25 19:12:19 UTC+0000                                 
    0x85969b00 spoolsv.exe            1208    400     14      293      0      0 2021-11-25 19:12:19 UTC+0000                                 
    0x859ae030 svchost.exe            1252    400     20      324      0      0 2021-11-25 19:12:19 UTC+0000                                 
    0x859d7488 vmicsvc.exe            1376    400      8      103      0      0 2021-11-25 19:12:19 UTC+0000                                 
    0x859de428 vmicsvc.exe            1396    400      7      108      0      0 2021-11-25 19:12:19 UTC+0000                                 
    0x859eaa60 vmicsvc.exe            1432    400      4       66      0      0 2021-11-25 19:12:19 UTC+0000                                 
    0x859ec4b8 taskhost.exe           1440    400     10      148      1      0 2021-11-25 19:12:19 UTC+0000                                 
    0x859f88b8 vmicsvc.exe            1504    400      5       80      0      0 2021-11-25 19:12:19 UTC+0000                                 
    0x85a13c60 dwm.exe                1532    848      5       85      1      0 2021-11-25 19:12:19 UTC+0000                                 
    0x85a25758 vmicsvc.exe            1540    400      6       81      0      0 2021-11-25 19:12:19 UTC+0000                                 
    0x85a1ab00 explorer.exe           1556   1512     25      587      1      0 2021-11-25 19:12:19 UTC+0000                                 
    0x85a42030 svchost.exe            1620    400     14      276      0      0 2021-11-25 19:12:19 UTC+0000                                 
    0x85a6d6f8 VBoxTray.exe           1716   1556     16      147      1      0 2021-11-25 19:12:20 UTC+0000                                 
    0x841e6470 cygrunsrv.exe          1872    400      6      100      0      0 2021-11-25 19:12:20 UTC+0000                                 
    0x85bf9b00 wlms.exe               1956    400      4       45      0      0 2021-11-25 19:12:20 UTC+0000                                 
    0x858cad28 cygrunsrv.exe          1612   1872      0 --------      0      0 2021-11-25 19:12:21 UTC+0000   2021-11-25 19:12:21 UTC+0000  
    0x858f2bc0 conhost.exe            1684    308      2       32      0      0 2021-11-25 19:12:21 UTC+0000                                 
    0x858d5d28 sshd.exe               1676   1612      4      100      0      0 2021-11-25 19:12:21 UTC+0000                                 
    0x85c54030 sppsvc.exe             1800    400      5      146      0      0 2021-11-25 19:12:22 UTC+0000                                 
    0x85c7e610 svchost.exe            2080    400      5       91      0      0 2021-11-25 19:12:22 UTC+0000                                 
    0x85d01d28 SearchIndexer.         2360    400     17      730      0      0 2021-11-25 19:12:26 UTC+0000                                 
    0x85d36d28 SearchProtocol         2440   2360      8      328      0      0 2021-11-25 19:12:26 UTC+0000                                 
    0x85d3a260 SearchFilterHo         2460   2360      6       95      0      0 2021-11-25 19:12:26 UTC+0000                                 
    0x85d16d28 csrss.exe              2616   2604     11      291      2      0 2021-11-25 19:12:33 UTC+0000                                 
    0x85873728 winlogon.exe           2644   2604      6      119      2      0 2021-11-25 19:12:33 UTC+0000                                 
    0x85d84b00 taskhost.exe           2784    400     11      172      2      0 2021-11-25 19:12:37 UTC+0000                                 
    0x85d8f488 dwm.exe                2844    848      5       89      2      0 2021-11-25 19:12:37 UTC+0000                                 
    0x85d91498 explorer.exe           2856   2836     27      700      2      0 2021-11-25 19:12:38 UTC+0000                                 
    0x85dacd28 regsvr32.exe           3108   2856      0 --------      2      0 2021-11-25 19:12:38 UTC+0000   2021-11-25 19:12:39 UTC+0000  
    0x84b3ed28 VBoxTray.exe           3504   2856     15      145      2      0 2021-11-25 19:12:46 UTC+0000                                 
    0x84b88788 WmiPrvSE.exe           3112    572      8      119      0      0 2021-11-25 19:13:24 UTC+0000                                 
    0x84bafc60 iexplore.exe           3324   2856     18      434      2      0 2021-11-25 19:13:31 UTC+0000                                 
    0x856aa9b8 iexplore.exe           3344   3324     26      641      2      0 2021-11-25 19:13:31 UTC+0000                                 
    0x8420dd28 powershell.exe         2700   3720     13      444      2      0 2021-11-25 19:13:50 UTC+0000                                 
    0x851733c8 conhost.exe            3732   2616      2       50      2      0 2021-11-25 19:13:50 UTC+0000                                 
    0x85d8db00 whoami.exe             4028   2700      0 --------      2      0 2021-11-25 19:14:01 UTC+0000   2021-11-25 19:14:01 UTC+0000  
    0x84289030 HOSTNAME.EXE           4036   2700      0 --------      2      0 2021-11-25 19:14:01 UTC+0000   2021-11-25 19:14:01 UTC+0000  
    0x84bee280 DumpIt.exe             2924   2856      2       37      2      0 2021-11-25 19:14:10 UTC+0000                                 
    0x84b046c0 conhost.exe            2920   2616      2       50      2      0 2021-11-25 19:14:10 UTC+0000                                 
    0x84ada2d0 dllhost.exe             168    572      6       88      2      0 2021-11-25 19:14:13 UTC+0000
    ```

    The malicious process is likely PPID (Parent Process ID) 2700 because it is running post-exploitation commands like `whoami.exe` and `HOSTNAME.EXE`.

3. We can find the full URL used to download the malware by first identifying the Internet Explorer (`iexplore.exe`) process(es) in the memory dump. I got the process ids for Internet Explorer with `./volatility_2.5_linux_x64 -f honeypot.raw --profile=Win7SP1x86 pslist | grep iexplore`. Then, I ran `./volatility_2.5_linux_x64 -f honeypot.raw --profile=Win7SP1x86 yarascan -Y "/(URL |REDR|LEAK)/" -p 2234,3344` to get the URLs that were accessed. I have copied the relevant output of this command below. You can learn more about this process using [this guide](https://volatility-labs.blogspot.com/2012/09/howto-scan-for-internet-cachehistory.html).

    ```
    Owner: Process iexplore.exe Pid 3344
    0x02805280  55 52 4c 20 02 00 00 00 a0 b1 00 94 30 e2 d7 01   URL.........0...
    0x02805290  a0 b1 00 94 30 e2 d7 01 95 53 ba 99 00 00 00 00   ....0....S......
    0x028052a0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
    0x028052b0  60 00 00 00 68 00 00 00 fe 00 10 10 00 00 00 00   `...h...........
    0x028052c0  01 00 20 00 ac 00 00 00 14 00 00 00 00 00 00 00   ................
    0x028052d0  79 53 ba 99 01 00 00 00 00 00 00 00 00 00 00 00   yS..............
    0x028052e0  00 00 00 00 ef be ad de 56 69 73 69 74 65 64 3a   ........Visited:
    0x028052f0  20 53 61 6e 74 61 40 68 74 74 70 73 3a 2f 2f 77   .Santa@https://w
    0x02805300  69 6e 64 6f 77 73 6c 69 76 65 75 70 64 61 74 65   indowsliveupdate
    0x02805310  72 2e 63 6f 6d 2f 63 68 72 69 73 74 6d 61 73 5f   r.com/christmas_
    0x02805320  75 70 64 61 74 65 2e 68 74 61 00 de 10 00 02 00   update.hta......
    0x02805330  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
    0x02805340  ef be ad de ef be ad de ef be ad de ef be ad de   ................
    0x02805350  ef be ad de ef be ad de ef be ad de ef be ad de   ................
    0x02805360  ef be ad de ef be ad de ef be ad de ef be ad de   ................
    0x02805370  ef be ad de ef be ad de ef be ad de ef be ad de   ................
    ```

    As you can see, the URL is `https://windowsliveupdater.com/christmas_update.hta`. We know this is the right URL because going to it redirects to the YouTube video for ["Rick Astley - Never Gonna Give You Up"](https://www.youtube.com/watch?v=dQw4w9WgXcQ).

4. Finally, we can get the attacker's IP address using `./volatility_2.5_linux_x64 -f honeypot.raw --profile=Win7SP1x86 netscan` (I found this command from [this blog post](https://www.andreafortuna.org/2017/07/24/volatility-my-own-cheatsheet-part-5-networking/)):

    ```
    Volatility Foundation Volatility Framework 2.5
    Offset(P)          Proto    Local Address                  Foreign Address      State            Pid      Owner          Created
    0x23d04218         TCPv4    0.0.0.0:49155                  0.0.0.0:0            LISTENING        400      services.exe   
    0x23d04218         TCPv6    :::49155                       :::0                 LISTENING        400      services.exe   
    0x2554b460         TCPv4    10.0.2.15:49226                93.184.220.29:80     ESTABLISHED      -1                      
    0x261e9d30         TCPv4    10.0.2.15:49228                172.67.177.22:443    ESTABLISHED      -1                      
    0x3e22f008         UDPv4    0.0.0.0:0                      *:*                                   2080     svchost.exe    2021-11-25 19:12:23 UTC+0000
    0x3e22f008         UDPv6    :::0                           *:*                                   2080     svchost.exe    2021-11-25 19:12:23 UTC+0000
    0x3e24c588         UDPv4    0.0.0.0:0                      *:*                                   2080     svchost.exe    2021-11-25 19:12:23 UTC+0000
    0x3e281368         UDPv4    10.0.2.15:138                  *:*                                   4        System         2021-11-25 19:12:23 UTC+0000
    0x3e2a29b8         UDPv4    0.0.0.0:0                      *:*                                   1084     svchost.exe    2021-11-25 19:12:23 UTC+0000
    0x3e2a29b8         UDPv6    :::0                           *:*                                   1084     svchost.exe    2021-11-25 19:12:23 UTC+0000
    0x3e2a6448         UDPv4    0.0.0.0:5355                   *:*                                   1084     svchost.exe    2021-11-25 19:12:26 UTC+0000
    0x3e354618         UDPv6    fe80::256b:4013:4140:453f:546  *:*                                   744      svchost.exe    2021-11-25 19:12:31 UTC+0000
    0x3e3b0c70         UDPv4    0.0.0.0:0                      *:*                                   2700     powershell.exe 2021-11-25 19:13:51 UTC+0000
    0x3e5e4f50         UDPv4    0.0.0.0:5355                   *:*                                   1084     svchost.exe    2021-11-25 19:12:26 UTC+0000
    0x3e5e4f50         UDPv6    :::5355                        *:*                                   1084     svchost.exe    2021-11-25 19:12:26 UTC+0000
    0x3e630008         UDPv4    0.0.0.0:0                      *:*                                   2700     powershell.exe 2021-11-25 19:13:51 UTC+0000
    0x3e630008         UDPv6    :::0                           *:*                                   2700     powershell.exe 2021-11-25 19:13:51 UTC+0000
    0x3e238300         TCPv4    0.0.0.0:445                    0.0.0.0:0            LISTENING        4        System         
    0x3e238300         TCPv6    :::445                         :::0                 LISTENING        4        System         
    0x3e2b5b88         TCPv4    10.0.2.15:139                  0.0.0.0:0            LISTENING        4        System         
    0x3e5f77a0         TCPv4    0.0.0.0:22                     0.0.0.0:0            LISTENING        1676     sshd.exe       
    0x3e619578         TCPv4    0.0.0.0:49152                  0.0.0.0:0            LISTENING        348      wininit.exe    
    0x3e619578         TCPv6    :::49152                       :::0                 LISTENING        348      wininit.exe    
    0x3e619cc0         TCPv4    0.0.0.0:49152                  0.0.0.0:0            LISTENING        348      wininit.exe    
    0x3e630a20         TCPv4    0.0.0.0:49156                  0.0.0.0:0            LISTENING        408      lsass.exe      
    0x3e630a20         TCPv6    :::49156                       :::0                 LISTENING        408      lsass.exe      
    0x3e648508         TCPv4    0.0.0.0:49153                  0.0.0.0:0            LISTENING        744      svchost.exe    
    0x3e648508         TCPv6    :::49153                       :::0                 LISTENING        744      svchost.exe    
    0x3e6b92c0         TCPv4    0.0.0.0:135                    0.0.0.0:0            LISTENING        692      svchost.exe    
    0x3e6b92c0         TCPv6    :::135                         :::0                 LISTENING        692      svchost.exe    
    0x3e6b9910         TCPv4    0.0.0.0:135                    0.0.0.0:0            LISTENING        692      svchost.exe    
    0x3e6f0bd8         TCPv4    0.0.0.0:49153                  0.0.0.0:0            LISTENING        744      svchost.exe    
    0x3e75f8e0         TCPv4    0.0.0.0:49154                  0.0.0.0:0            LISTENING        888      svchost.exe    
    0x3e762a40         TCPv4    0.0.0.0:49155                  0.0.0.0:0            LISTENING        400      services.exe   
    0x3e7686e8         TCPv4    0.0.0.0:49154                  0.0.0.0:0            LISTENING        888      svchost.exe    
    0x3e7686e8         TCPv6    :::49154                       :::0                 LISTENING        888      svchost.exe    
    0x3e2e9cc0         TCPv4    10.0.2.15:49221                212.205.126.106:443  ESTABLISHED      -1                      
    0x3ed036c8         UDPv4    10.0.2.15:137                  *:*                                   4        System         2021-11-25 19:12:23 UTC+0000
    0x3e8611f0         TCPv4    0.0.0.0:22                     0.0.0.0:0            LISTENING        1676     sshd.exe       
    0x3e8611f0         TCPv6    :::22                          :::0                 LISTENING        1676     sshd.exe       
    0x3e9be828         TCPv4    0.0.0.0:49156                  0.0.0.0:0            LISTENING        408      lsass.exe      
    0x3ee98d80         TCPv4    10.0.2.15:49229                147.182.172.189:4444 ESTABLISHED      -1                      
    0x3f1b0df8         TCPv4    10.0.2.15:49216                212.205.126.106:443  ESTABLISHED      -1                      
    0x3f2cff50         UDPv4    0.0.0.0:0                      *:*                                   261576   ??            2021-11-25 19:13:04 UTC+0000
    0x3f2cff50         UDPv6    :::0                           *:*                                   261576   ??            2021-11-25 19:13:04 UTC+0000
    0x3f4d7378         UDPv4    0.0.0.0:0                      *:*                                   2700     powershell.exe 2021-11-25 19:13:51 UTC+0000
    0x3f4dad28         UDPv4    127.0.0.1:58426                *:*                                   3344     iexplore.exe   2021-11-25 19:13:31 UTC+0000
    0x3f520ab8         UDPv4    0.0.0.0:0                      *:*                                   2700     powershell.exe 2021-11-25 19:13:51 UTC+0000
    0x3f520ab8         UDPv6    :::0                           *:*                                   2700     powershell.exe 2021-11-25 19:13:51 UTC+0000
    0x3f546de8         UDPv4    0.0.0.0:0                      *:*                                   636      VBoxService.ex 2021-11-25 19:14:14 UTC+0000
    0x3f225df8         TCPv4    10.0.2.15:49222                212.205.126.106:443  ESTABLISHED      -1                      
    0x3f547008         TCPv4    10.0.2.15:49220                212.205.126.106:443  ESTABLISHED      -1                      
    0x3f561438         TCPv4    10.0.2.15:49215                204.79.197.203:443   ESTABLISHED      -1                      
    0x3f57c438         TCPv4    10.0.2.15:49218                95.100.210.141:443   ESTABLISHED      -1                      
    0x3f58b4c8         TCPv4    10.0.2.15:49217                212.205.126.106:443  ESTABLISHED      -1                      
    0x3f58c748         TCPv4    10.0.2.15:49223                212.205.126.106:443  ESTABLISHED      -1                      
    0x3f58e9d8         TCPv4    10.0.2.15:49225                172.67.177.22:443    ESTABLISHED      -1                      
    0x3f5c6df8         TCPv4    10.0.2.15:49219                95.100.210.141:443   ESTABLISHED      -1                      
    ```

    In the foreign address column we see a connection from an IP address on port `4444`: `147.182.172.189:4444`. This is the default port used in metasploit so it is likely the attacker's IP since no normal traffic is sent over this port. So, the attacker's IP is `147.182.172.189`. This output also provides more evidence that PPID `2700` is the correct malicious process ID.

5. We can now generate the flag: `echo -n "https://windowsliveupdater.com/christmas_update.hta_2700_147.182.172.189" | md5sum` outputs `969b934d7396d043a50a37b70e1e010a`, so the flag is `HTB{969b934d7396d043a50a37b70e1e010a}`.


### Flag

`HTB{969b934d7396d043a50a37b70e1e010a}`
