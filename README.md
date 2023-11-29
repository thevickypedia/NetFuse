# DNS Resolver

DNS Resolver is a python script that dumps hostname and IP address mapping for localhost into host file

### Usage

```python
import netsync

netsync.dump(netsync.SupportedSystems.att)
```

### Note

> This is a hacky solution for a real problem. The best approach would be [run your own DNS server][howto]

[howto]: https://www.howtogeek.com/devops/how-to-run-your-own-dns-server-on-your-local-network/
