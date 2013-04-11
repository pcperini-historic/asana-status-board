import threading
 
def _async(func, *a, **kw):
    thread = threading.Thread(target = func, args = a, kwargs = kw)
    thread.start()
    return thread
 
def async(func):
    return lambda *a, **kw: _async(func, *a, **kw)