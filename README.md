## Linting

```console
$ python -m venv env
$ source env/bin/activate
$ pip install -e '.[dev]'
$ make -j $(nproc) lint
```
