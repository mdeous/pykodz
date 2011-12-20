#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread
from time import sleep

class async(Thread):

    def __init__(self, callback, errback):
        super(async, self).__init__()
        self.callback = callback
        self.errback = errback

    def __call__(self, func):
        # à l'appel de la fonction, on récupère juste la fonction
        # et ses arguments, et on lance notre thread
        def wrapper(*args, **kwargs):
            self.func = func
            self.args = args
            self.kwargs = kwargs
            self.start()
        return wrapper

    def run(self):
        try:
            retval = self.func(*self.args, **self.kwargs)
            self.callback(retval)
        except Exception as err:
            self.errback(err)


def my_callback(retval):
    print "CALLBACK:", retval
    # ici on peut faire des opérations supplémentaires
    # sur la valeur renvoyée par la fonction.
    # ce code est appelé par le thread, il ne peut donc
    # pas bloquer notre thread principal

def my_errback(err):
    print "ERRBACK", err
    # ici on peut re-lancer l'exception, ou simplement
    # l'ignorer. Ce code est également appelé dans le thread


@async(my_callback, my_errback)
def ma_fonction_reussie(n):
    sleep(n)
    return n

@async(my_callback, my_errback)
def ma_fonction_foireuse(n):
    sleep(n)
    raise AttributeError("Got %s, expected 'foo'" % n)


ma_fonction_reussie(5)
ma_fonction_foireuse(7)

# histoire de passer le temps pendant ce temps là...
for i in range(10):
    print "MAIN:", i
    sleep(1)
