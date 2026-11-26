# Neon Migration Toolkit

Read-only SQLite migration inventory and typed JSONL export for planning PostgreSQL and Neon migrations.

![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white) ![License MIT](https://img.shields.io/badge/License-MIT-green)

## Quick start

Python 3.10+; standard library only. Clone or extract the repository, then run from its root.

```bash
python3 migrate.py ./dev.db
python3 migrate.py ./dev.db --export-dir ./private-export
```

## Scope and limitations

Inventory and export only; does not connect to Neon, generate or execute PostgreSQL DDL, or promise type parity. JSONL rows use manifest column order for ordinary tables; generated/hidden columns, views, virtual tables, indexes, triggers and custom collations need separate migration work. Export contains unredacted database contents; never commit it. Use a private directory and validate row counts, constraints and application behavior on a disposable destination. On export failure, incomplete output must be discarded manually.



## Development

```bash
python3 -m unittest discover -s tests -v
```



## Contributing and security

See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md). Please do not publish real credentials, customer data or sensitive reports in issues.

## License

MIT — see [LICENSE](LICENSE).
