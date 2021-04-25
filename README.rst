simpleclock
===========
.. code-block:: python

    import logging

    import simpleclock as sc

    since = sc.Since(logger=logging.getLogger())
    start = sc.ts()

    # some code 1

    ts = since(start).print("first")  # >>> first: 10.00s

    # some code 2

    ts = since(ts).info("some code 2 took")  # >>> 1970-01-01 00:00:40,000 - root - INFO - some code 2 took: 30.00s

    # some code 3

    since(ts).duration  # ~ 2.
    since(start).duration  # ~ 42.
