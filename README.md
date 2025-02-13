# esatools

## Quickstart
1. Install `esatools` package.
```bash
pip install git+https://github.com/t-sasatani/esatools.git
```

2. Set read tokens. Copy `.example.env` (below) to `.env` in the current directory and populate ESA_ACCESS_TOKEN (read-only esa.io token) and ESA_CURRENT_TEAM.
```env
ESA_ACCESS_TOKEN=your_access_token
ESA_CURRENT_TEAM=your_team_name

ESATOOLS_EXPORT_DIR=./backup
ESATOOLS_LOG_LEVEL=INFO
```

3. Run `backup` command.
```bash
esatools backup
```

then the markdown files from esa.io is fetched to `ESATOOLS_EXPORT_DIR` with the same directory format as `esa.io`.
