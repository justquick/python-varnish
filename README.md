### Simple Python interface for the Varnish management port.

Varnish is a state-of-the-art, high-performance HTTP accelerator.
For more information checkout [http://varnish.projects.linpro.no/](http://varnish.projects.linpro.no/)

Varnish provides a simple telnet management interface for doing things like:

  *  reloading configurations
  *  purging URLs from cache
  *  view statistics
  *  start and stop the server

This Python API takes full advantage of the available commands and can run
across multiple Varnish instances

Example:

    >>> manager = VarnishManager( ('server1:82', 'server2:82') )
    >>> print manager.run('stats')
    >>> manager.close()