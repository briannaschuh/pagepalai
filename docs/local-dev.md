
# Local Development Notes

Notes for myself on maintaining the project locally

## Running Tests

### Using `pytest`

```bash
# From project root
PYTHONPATH=. pytest
```
### Test File Notes
- Test files should be named `test_*.py` or `*_test.py`
- Use `assert` instead of print statements when defining tests
- Tests live in `/tests/` folder

## DB Setup & Usage

### Create Tables
```python
# run once at project start
from backend.db.init_db import create_tables
create_tables()
```

### Generic DB Functions (in `db.py`)
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
