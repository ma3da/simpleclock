simpleclock
===========
.. code-block:: python

    import simpleclock

    clock = Clock.started()

    # some code 1

    clock.elapsed_since_start.print()  # >>> elapsed since start: <duration1>s

    # some code 2

    clock.silent.elapsed_since_last_call.print("some code 2 took")  # >>> some code 2 took: <duration2>s

    # some code 3

    clock.elapsed_since_last_call()  # ~ duration2 + duration3
    clock.elapsed_since_last_call()  # ~ 0
    clock.elapsed_since_start()      # ~ duration1 + ... + duration3

