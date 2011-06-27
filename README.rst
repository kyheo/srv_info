SRV_INFO
========
The main idea behind this is to have a central place where all *clients* can
notify events.

It will run on `Google Appengine`_ service, using the Python_ SDK_.

How does it works
=================
In fact, how it will work :).

This system will provide an API (restFull, restLike, or whatever) to where the
clients will send the different events. There will be a web interface, for the
user to see the stored information.

Store and filter server events are my personal needs, in the future it will be
nice to have other things like stats or graphs, but I settle with a white page
with a list of events.

Contact
=======
You can reach me by email at marrese@gmail.com.

.. _`Google Appengine`: https://appengine.google.com/
.. _Python: http://www.python.org/
.. _SDK: http://code.google.com/appengine/docs/python/
