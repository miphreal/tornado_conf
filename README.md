### Tornado Settings

#### Instalation

```bash
$ pip install tornado_conf
```

#### Usage

Project structure:

    ◉ project root/
    ├ <project_name>/
    │ ├ ...
    │ ├ settings/
    │ │ ├ __init__.py
    │ │ ├ server.cfg
    │ │ ├ base.py
    │ │ ├ local.py
    │ │ ├ prod.py
    │ │ └ qa.py
    │ ├ ...
    │ └ app.py
    ├ ...
    ├ LICENSE
    ├ README
    └ .gitignore
    
    
_settings/base.py:_
```python
setting1 = 'base setting'
SETTING = 'COMMON'
```

_settings/local.py:_
```python    
from .base import *

setting1 = 'local setting'
```

_settings/prod.py:_
```python    
from .base import *

setting1 = 'prod setting'
SETTING = 'PROD'
```

_app.py:_
```python
import tornado.ioloop
import tornado.web
from tornado.options import options

from tornado_conf import setup_settings, settings

# ...

if __name__ == '__main__':
    setup_settings(settings_package='settings')
    options.parse_config_file('settings/server.cfg', final=False)
    options.parse_command_line()

    print settings.SETTING, settings.setting1

    application = tornado.web.Application([
        # ...
    ], **settings)

    application.listen(8765)
    tornado.ioloop.IOLoop.instance().start()
```

Shell:
    
    $ python app.py
    COMMON base setting

    $ python app.py --settings=local
    COMMON local setting
    
    $ python app.py --settings=prod
    PROD prod setting
    
    $ python app.py --settings=unknown
    Traceback (most recent call last):
      ...
    ImportError: No module named unknown
