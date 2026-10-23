# Web Form Automation

Pytest and Selenium checks for the practice form at `https://www.qapractice.com/practice-forms`.
The tests use synthetic data only; the site states that submitted data is not stored.

## Requirements

- Python 3.10 or newer
- Google Chrome or Microsoft Edge

## Install

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run tests

Run the full suite in the browser configured in `config/config.json`:

```powershell
pytest
```

Run headlessly or select a browser:

```powershell
pytest --headless
pytest --browser edge --headless
```

Run only the smoke or negative-validation checks:

```powershell
pytest -m smoke
pytest -m negative
```

The pytest HTML report is generated at `reports/report.html`; failure and submission
screenshots are written under `reports/screenshots/`. These generated artifacts are
excluded from version control.

## Project layout

- `pages/`: Page objects and shared Selenium interactions
- `tests/`: Pytest and unittest cases
- `data/`: Synthetic CSV and JSON test inputs
- `config/config.json`: Target URL, browser, and explicit wait setting
- `utilities/`: Configuration, data, and logging helpers
