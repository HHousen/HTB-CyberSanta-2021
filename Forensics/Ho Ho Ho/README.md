# Ho Ho Ho (750)

## Problem

> Santa, Santa, where are you? Are you hidden in the private and the public too? Riddle, riddle, what am I? Find me and I'll give you what is mine.

* [forensics_ho_ho_ho.zip](./forensics_ho_ho_ho.zip)

## Solution

1. We are given a PCAP, so let's open it in Wireshark.

2. If we sort to only see HTTP traffic by applying the `http` filter, we see that several requests are made to the `/yDENnwqMdkhG9yjj9bJN` endpoint with a parameter equal to a single byte in the form `/yDENnwqMdkhG9yjj9bJN?=D5`.

3. If we append all those parameters in the URL we get `D5476E6849AEF8A8c568BD7E47cF6647C8C98485`. This looks like hexadecimal, but strangely it is formatted with nearly all capital letters except two `c`s.

4. This is an Ethereum address on the Ropsten test network. For this challenge, I believe you just have to recognize this since there are no other hints. We can look it up on [ropsten.etherscan.io](https://ropsten.etherscan.io/address/0xD5476E6849AEF8A8c568BD7E47cF6647C8C98485).

5. If we look at one of the transactions that were made involving this address, we see that there is content in the "Input Data" field, which is commonly used as a message associated with a transaction. We can see all the transactions on the [transactions page](https://ropsten.etherscan.io/txs?a=0xD5476E6849AEF8A8c568BD7E47cF6647C8C98485&f=2) and filter by outbound transactions.

6. Going through all 59 transactions and viewing the input data as "UTF-8" reveals the following message (4 characters per transaction): `We are going to get exposed! You should wipe all evidence and enable the ransom killswitch: HTB{54nt4_c4nn0t_tr4c3_th3_m0n3y_r1ght??!}. They hired those technerds to find us but they didn't know that we are better cypherpunks than them!`. The message has the flag within it.

7. It is possible to script the act of getting the input data for all 59 transactions, either by using an API to a blockchain explorer that supports the Ropsten test network, by actually downloading part of the blockchain, or by automating a web browser to visit the transaction pages on [ropsten.etherscan.io](https://ropsten.etherscan.io/address/0xD5476E6849AEF8A8c568BD7E47cF6647C8C98485) and copy the input data. However, writing a script to do this would have taken longer than doing it manually.

### Flag

`HTB{54nt4_c4nn0t_tr4c3_th3_m0n3y_r1ght??!}`
