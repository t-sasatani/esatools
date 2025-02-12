# esa-fetch

## Quickstart
```bash
pip install git+https://github.com/t-sasatani/esa-tools.git
```
Copy `.example.env` to `.env` and fill in esa.io token, esa username, and export directory.
```bash
esatools fetch
```
then the markdown files from esa.io is fetched to `ESATOOLS_EXPORT_DIR` with the same directory format as `esa.io`.