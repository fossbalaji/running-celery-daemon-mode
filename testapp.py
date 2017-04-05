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


