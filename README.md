# NetFuse

NetFuse is a python module to dump hostname and IP address mapping for localhost into the hosts file

> :warning: &nbsp; To use this module, the router should be `Netgear`, [OR] the ISP should be `At&t`

### Installation
```shell
pip install NetFuse
```

### Usage

> :bulb: &nbsp; Use `netfuse --help` to learn more

```shell
sudo netfuse
```

### Note

> This is a hacky solution for a real problem. The best approach would be to [run your own DNS server][howto]

[howto]: https://www.howtogeek.com/devops/how-to-run-your-own-dns-server-on-your-local-network/
