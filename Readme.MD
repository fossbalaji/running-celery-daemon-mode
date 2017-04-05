####Running celery in Daemon##########

# Instalation 

`sudo apt-get install python-celery celeryd`

* Prerequiste:
    * rabbitmq (see [here](https://www.rabbitmq.com/download.html))

    * celery (`pip install celery`)

# Sample celery app

save this as `testapp.py`

```shell
from __future__ import absolute_import
from celery import Celery
import sys
import time


celery_url = "amqp://%s:%s@%s//" % ("guest", "guest", "0.0.0.0")

celery_app = Celery("testapp", broker=celery_url,
                backend='rpc://')


@celery_app.task()
def add(x,y):
    print "hi from task add", x, y
    return x+y


def main(x,y):
    """
        This is main function gets called initially while running 
    """
    print "Let's add %s and %s" % (x, y)
    res = add.apply_async(args=[x, y])
    time.sleep(3)
    if res.ready():
        print "Result from task %s" % res.result



if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: python testapp.py 1 2"
        sys.exit(0)
    x = int(sys.argv[1])
    y = int(sys.argv[2])
    main(x,y)
```

# Configure celeryd in `/etc/default/celeryd`

If you have installed `celeryd` it created daemon script in `/etc/default/celeryd`.

change/add these lines in `/etc/default/celeryd`

```shell
ENABLED="true" # enable daemon mode
CELERYD_CHDIR="/home/bala/personal/celery-daemon"
# change above line to the directory which contains our testapp.py
CELERYD_OPTS="--app=testapp --loglevel=info --time-limit=300 --concurrency=8"
```

Now restart celeryd to reflect config changes 

`sudo service celeryd restart`


which results like this

```shell
celery multi v3.1.6 (Cipater)
> Starting nodes...
    > w1@bala: OK
```
you can check the logs in `/var/log/celery/w1.log`

# Run python file by `python testapp.py 2 3`

which gives us 

```shell
Let's add 2 and 3
Result from task 5
```