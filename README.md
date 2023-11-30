[![pypi](https://github.com/thevickypedia/NetFuse/actions/workflows/python-publish.yml/badge.svg)][gh_pypi]
[![pages](https://github.com/thevickypedia/NetFuse/actions/workflows/pages/pages-build-deployment/badge.svg)][gh_pages]

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


## Coding Standards
Docstring format: [`Google`][google-docs] <br>
Styling conventions: [`PEP 8`][pep8] and [`isort`][isort]

## [Release Notes][release-notes]
**Requirement**
```shell
python -m pip install gitverse
```

**Usage**
```shell
gitverse-release reverse -f release_notes.rst -t 'Release Notes'
```

## Linting
`pre-commit` will ensure linting, run pytest, generate runbook & release notes, and validate hyperlinks in ALL
markdown files (including Wiki pages)

**Requirement**
```shell
pip install sphinx==5.1.1 pre-commit recommonmark
```

**Usage**
```shell
pre-commit run --all-files
```

## Pypi Package
[![pypi-module](https://img.shields.io/badge/Software%20Repository-pypi-1f425f.svg)][pypi-repo]

[https://pypi.org/project/NetFuse/][pypi]

## Runbook
[![made-with-sphinx-doc](https://img.shields.io/badge/Code%20Docs-Sphinx-1f425f.svg)][sphinx]

[https://thevickypedia.github.io/NetFuse/][runbook]

## License & copyright

&copy; Vignesh Rao

Licensed under the [MIT License][license]

[howto]: https://www.howtogeek.com/devops/how-to-run-your-own-dns-server-on-your-local-network/

[gh_pypi]: https://github.com/thevickypedia/NetFuse/actions/workflows/python-publish.yml
[gh_pages]: https://github.com/thevickypedia/NetFuse/actions/workflows/pages/pages-build-deployment

[google-docs]: https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
[pep8]: https://www.python.org/dev/peps/pep-0008/
[isort]: https://pycqa.github.io/isort/
[sphinx]: https://www.sphinx-doc.org/en/master/man/sphinx-autogen.html
[pypi-repo]: https://packaging.python.org/tutorials/packaging-projects/

[runbook]: https://thevickypedia.github.io/NetFuse/
[pypi]: https://pypi.org/project/NetFuse/
[release-notes]: https://github.com/thevickypedia/NetFuse/blob/main/release_notes.rst
[license]: https://github.com/thevickypedia/NetFuse/blob/main/LICENSE
