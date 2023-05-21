# Utilities
## `config.py`
```Python
from config import config # import
cfg = config("./path/to/json") # load and parse json file to dict
cfg_p = config("./path/to/json")["secret"] # access like dict
```
## `utility.py`
```Python
import utility
html = utility.rdoc("./path/to/html") # load file as string
```
## `log.py`
```Python
from log import setup_logger
logger = setup_logger("authorize_server") # setup pre-configured standard Python logger
```
# Public APIs
## `authorization.py`
```Python
import authorization
aserver = authorization() # init authorization server
# in development
```
