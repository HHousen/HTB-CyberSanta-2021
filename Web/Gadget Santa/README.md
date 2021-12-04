# Gadget Santa (300)

## Problem

> It seems that the evil elves have broken the controller gadget for the good old candy cane factory! Can you team up with the real red teamer Santa to hack back?

* [web_gadget_santa.zip](./web_gadget_santa.zip)

## Solution

1. The website allows us to view some properties about a linux system. The output looks just like standard linux commands. The output of the "List Storage" command seems to be executing `df -h`.

2. At this point, I guessed that this was a command injection challenge and I tried accessing `http://IP:PORT/?command=ls"` to see if I could list the contents of the current directory. Sure enough, this worked, confirming my suspicions. This is in fact a command injection challenge.

3. Looking at the source code, we see in `challenge/models/MonitorModel.php` that `shell_exec` is used to run the `santa_mon.sh` script. Our input in the `command` URL parameter is then appended to `/santa_mon.sh ` so that the final command looks like this: `/santa_mon.sh [COMMAND PARAMETER INPUT]`. In other words, we control the first argument passed to the `santa_mon.sh` program. Importantly, The `sanitize` function is called on our input, which removes spaces using the `s+` regular expression.

4. We can see the source code of the `santa_mon.sh` program in `config/santa_mon.sh` in our downloaded ZIP. We see that the buttons in the web interface do indeed run standard linux commands. At the bottom we see that if there is an argument to the program, it is executed as a command.

5. `config/santa_mon.sh` shows that the `ups_status` and `restart_ups` commands return the output from a local web server using curl. If you check the output of the "List Processes" command you will see `python3 /root/ups_manager.py`. Let's check out the source code for `config/ups_manager.py`. This file runs an HTTP server with the two endpoints accessed by the `ups_status` and `restart_ups` commands, but it also has a `/get_flag` endpoint that prints the flag!

6. So, our approach to get the flag is to craft a command injection payload without using spaces that will run `curl http://localhost:3000/get_flag` and return the output to us through the webpage. Using a standard approach to remove spaces (such as those from the excellent guide at [swisskyrepo/PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Command%20Injection#bypass-without-space)) will not work here because our input is stripped of whitespace and then passed as an argument to another program. Thus, use can use something like the `IFS` variable, since hte PHP code will not strip that out, but when it is parsed by bash it will be interpreted as a second argument to the `santa_mon.sh` script. For instance, if our command injection is `curl${IFS}http://localhost:3000/get_flag` then PHP will execute, `/santa_mon.sh curl${IFS}http://localhost:3000/get_flag`, bash will interpret this as `/santa_mon.sh curl http://localhost:3000/get_flag`, and then the `santa_mon.sh` script will see `curl` as the first argument and will run `curl` without any arguments.

7. To solve this, we simply wrap our payload in double quotes like so: `"curl${IFS}http://localhost:3000/get_flag"` (URL encoded: `%22curl${IFS}http://localhost:3000/get_flag%22`). This way, PHP will execute `/santa_mon.sh "curl${IFS}http://localhost:3000/get_flag"`, bash will interpret this as `/santa_mon.sh "curl http://localhost:3000/get_flag"`, then the `santa_mon.sh` script will see the string `"curl http://localhost:3000/get_flag"` as the first parameter, it will run our payload, and the PHP server will return the output containing the flag.

8. So, the final payload is `http://IP:PORT/?command=%22curl${IFS}http://localhost:3000/get_flag%22`.

### Flag

`HTB{54nt4_i5_th3_r34l_r3d_t34m3r}`
