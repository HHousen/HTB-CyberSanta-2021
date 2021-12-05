# Giveaway (300)

## Problem

> Santa's SOC team is working overtime during December due to Christmas phishing campaigns. A new team of malicious actors is targeting mainly those affected by the holiday spirit. Could you analyse the document and find the command & control server?

* [forensics_giveaway.zip](./forensics_giveaway.zip)

## Solution

1. The challenge is a ".docm" file, which is a [Microsoft Word Macro-enabled Document](https://fileinfo.com/extension/docm).

2. You can look at these macros in a program like Microsoft Word or LibreOffice Writer. In LibreOffice, I went to Tools > Macros > Edit Macros, and starting looking around. Within the the "Edit Macros" dialogue, I went to `"christmas_giveaway.docm" > Project > Document Objects > ThisDocument`. We are asked to find the command & control server, so we're searching for a URL.

3. In the `Auto_Open` function, I found the text `https://` and then what looks like an obfuscated URL:

    ```
    HPkXUcxLcAoMHOlj = "https://elvesfactory/" & Chr(Asc("H")) & Chr(84) & Chr(Asc("B")) & "" & Chr(123) & "" & Chr(84) & Chr(Asc("h")) & "1" & Chr(125 - 10) & Chr(Asc("_")) & "1s" & Chr(95) & "4"
     cxPZSGdIQDAdRVpziKf = "_" & Replace("present", "e", "3") & Chr(85 + 10)
     fqtSMHFlkYeyLfs = Replace("everybody", "e", "3")
     fqtSMHFlkYeyLfs = Replace(fqtSMHFlkYeyLfs, "o", "0") & "_"
     ehPsgfAcWaYrJm = Chr(Asc("w")) & "4" & Chr(110) & "t" & Chr(115) & "_" & Chr(Asc("f")) & "0" & Chr(121 - 7) & Chr(95)
     FVpHoEqBKnhPO = Replace("christmas", "i", "1")
     FVpHoEqBKnhPO = Replace(FVpHoEqBKnhPO, "a", "4") & Chr(119 + 6)

     Open XPFILEDIR For Output As #FileNumber
     Print #FileNumber, "strRT = HPkXUcxLcAoMHOlj & cxPZSGdIQDAdRVpziKf & fqtSMHFlkYeyLfs & ehPsgfAcWaYrJm & FVpHoEqBKnhPO"
    ```

4. It looks like the `Chr` function is the same as the `chr` function in Python and the `Asc` function is the same as the `ord` function in Python. In other words, `Chr` converts decimal to ASCII and `Asc` converts ASCII to decimal. `Replace` replaces every substring specified by the second argument with the third argument in the first argument. Finally `&` concatenates strings.

5. I manually deobfuscated this code like so:

    ```
    HPkXUcxLcAoMHOlj = "https://elvesfactory/HTB{Th1s_1s_4"
    cxPZSGdIQDAdRVpziKf = "_pr3s3nt_"
    fqtSMHFlkYeyLfs = "3v3rybody"
    fqtSMHFlkYeyLfs = "3v3ryb0dy_"
    ehPsgfAcWaYrJm = "w4nts_f0r_"
    FVpHoEqBKnhPO = "chr1stmas"
    FVpHoEqBKnhPO = "chr1stm4s}"
    Print #FileNumber, "strRT = HPkXUcxLcAoMHOlj & cxPZSGdIQDAdRVpziKf & fqtSMHFlkYeyLfs & ehPsgfAcWaYrJm & FVpHoEqBKnhPO"
    ```

6. This reveals that the flag is everything after "https://elvesfactory/" in the `strRT` variable.

7. Instead of reversing this code, you could use [OnlineGDB's VB Compiler](https://www.onlinegdb.com/online_vb_compiler) to run the macro and use `Console.WriteLine()` to print the flag.

### Flag

`HTB{Th1s_1s_4_pr3s3nt_3v3ryb0dy_w4nts_f0r_chr1stm4s}`
