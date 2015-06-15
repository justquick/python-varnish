Simple Python interface for the Varnish management port
=========================================================


:Author:
   Justin Quick <justquick@gmail.com>, Sandy Walsh <github@darksecretsoftware.com>
:Version: 0.2

::

    pip install python-varnish==0.2.1

If you are running a version of varnish older than 3.0 then install python-varnish==0.1.2 instead.

Varnish is a state-of-the-art, high-performance HTTP accelerator.
For more information checkout `Varnish Site <http://varnish.projects.linpro.no/>`_

Varnish provides a simple telnet management interface for doing things like:

  *  reloading configurations
  *  purging URLs from cache
  *  view statistics
  *  start and stop the server

This Python API takes full advantage of the available commands and can run
across multiple Varnish instances. Here are the features of this python module
(compared to `python-varnishadm <http://varnish.projects.linpro.no/browser/trunk/varnish-tools/python-varnishadm/>`_)

  *  Uses ``telnetlib`` instead of raw sockets
  *  Implements ``threading`` module
  *  Can run commands across multiple Varnish instances
  *  More comprehensive methods, closely matching the management API (``purge_*``, ``vcl_*``, etc.)
  *  Unittests

Example::

  manager = VarnishManager( ('server1:6082', 'server2:6082') )
  manager.run('ping')
  manager.run('ban.url', '^/secret/$')
  manager.run('ban.list')
  manager.run('purge.url', 'http://mydomain.com/articles/.*')
  manager.close()

Testing::

  python runtests.py
