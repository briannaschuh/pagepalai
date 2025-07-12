
# Local Development Notes

Notes for myself on maintaining the project locally

## Running Tests

### Using `pytest`

Below will test all tests in the `/tests` folder
```bash
# From project root
PYTHONPATH=. pytest
```
Below is an example of how to test a specific file
```bash
PYTHONPATH=. pytest tests/test_books_db.py
```
Below is an example of how to test a specific function inside a specific file
```bash
PYTHONPATH=. pytest tests/test_chunks_db.py -k test_chunks_table_crud
```
### Test File Notes
- Test files should be named `test_*.py` or `*_test.py`
- Use `assert` instead of print statements when defining tests
- Tests live in `/tests/` folder

## DB Setup & Usage

## Region

In the `.env` file, there is a boolean variable used to decide which DB should be used.
```bash
USE_REMOTE_DB=False
```
Set it to false when running locally. In prod, that variable should be set to True.

### Create Tables
```python
# run once at project start
from backend.db.init_db import create_tables
create_tables()
```

### DB Functions (in `db.py`)
- `insert(table_name, columns, values)`
- `select(table_name, columns="*", condition=dict)`
- `update(table_name, data=dict, update_condition=dict)`
- `delete(table_name, condition=dict)`
- `exists(table_name, condition=dict)`

## Logging

### Global logging is configured in `app.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
)
```

### In every other file:

```python
import logging
log = logging.getLogger(__name__)
```
