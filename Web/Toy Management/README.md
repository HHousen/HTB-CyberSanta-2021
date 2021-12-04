# Toy Management (300)

## Problem

> The evil elves have changed the admin access to Santa's Toy Management Portal. Can you get the access back and save the Christmas?

* [web_toy_management.zip](./web_toy_management.zip)

## Solution

1. The website is a simple login page.

2. After looking at the source code for a while, I noticed that the `database.sql` file contains the password hashes for a manager and admin user. [CrackStation](https://crackstation.net/) is a great way to see if these are known hashes, so I pasted them both in and got the credentials `manager:bigsanta!` and `admin:tryharder`.

3. `manager:bigsanta!` is a valid login by `admin:tryharder` is not. After signing in we can see a list of toys and some other properties.

4. Looking back at the source code in the `database.sql` file we see that the flag is contained in the database with the rest of the toys, but it has the approved value set to 0 instead of 1.

5. In `challenge/routes/index.js` we see that the `/api/toylist` endpoint will set `approved` to 1 unless the currently signed in user has the username `admin`. So, we have to sign in as admin.

6. My first thought was that this was a JWT challenge since JWTs are used and we are given a user with valid credentials. However, after poking around, the `database.js` source code shows that users are authenticated like so: `let stmt = "SELECT username FROM users WHERE username = '${user}' and password = '${pass}'\";`. This looks like it could be vulnerable to a SQL injection.

7. On the main login page, I tried some common SQL injection payloads from [swisskyrepo/PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection#authentication-bypass). The one that ended up working was username `admin' -- ` and the password can be anything. This will show us the final "unapproved toy" which is the flag.

### Flag

`HTB{1nj3cti0n_1s_in3v1t4bl3}`
