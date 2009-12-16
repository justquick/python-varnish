Simple Python interface for the Varnish management port
=========================================================

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
  manager.run('purge.url', '^/$')
  manager.close()