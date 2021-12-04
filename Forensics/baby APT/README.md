# baby APT (300)

## Problem

> This is the most wonderful time of the year, but not for Santa's incident response team. Since Santa went digital, everyone can write a letter to him using his brand new website. Apparently an APT group hacked their way in to Santa's server and destroyed his present list. Could you investigate what happened?

* [forensics_baby_apt.zip](./forensics_baby_apt.zip)

## Solution

1. So, we could analyze this PCAP in Wireshark, but I like to try for easy wins on [A-Packets](https://apackets.com/) first since it allows more easy navigation of HTTP data.

2. I uploaded the PCAP to [A-Packets](https://apackets.com/) and went to the HTTP flows page.

3. Looking through the requests made it seems like someone found a command injection vulnerability on this webpage.

4. Eventually, towards the end of the steams, the attacker sent this payload: `cmd=rm++%2Fvar%2Fwww%2Fhtml%2Fsites%2Fdefault%2Ffiles%2F.ht.sqlite+%26%26+echo+SFRCezBrX24wd18zdjNyeTBuM19oNHNfdDBfZHIwcF8wZmZfdGgzaXJfbDN0dDNyc180dF90aDNfcDBzdF8wZmYxYzNfNGc0MW59+%3E+%2Fdev%2Fnull+2%3E%261+%26%26+ls+-al++%2Fvar%2Fwww%2Fhtml%2Fsites%2Fdefault%2Ffiles`.

5. I used [urldecoder.org](https://www.urldecoder.org/) to make this easier to read: `cmd=rm++/var/www/html/sites/default/files/.ht.sqlite+&&+echo+SFRCezBrX24wd18zdjNyeTBuM19oNHNfdDBfZHIwcF8wZmZfdGgzaXJfbDN0dDNyc180dF90aDNfcDBzdF8wZmYxYzNfNGc0MW59+>+/dev/null+2>&1+&&+ls+-al++/var/www/html/sites/default/files`.

6. Part of this command is to `echo` the string `SFRCezBrX24wd18zdjNyeTBuM19oNHNfdDBfZHIwcF8wZmZfdGgzaXJfbDN0dDNyc180dF90aDNfcDBzdF8wZmYxYzNfNGc0MW59` to `/dev/null`. [Decoding this string as base64](https://www.base64decode.org/) reveals the flag.

### Flag

`HTB{0k_n0w_3v3ry0n3_h4s_t0_dr0p_0ff_th3ir_l3tt3rs_4t_th3_p0st_0ff1c3_4g41n}`
