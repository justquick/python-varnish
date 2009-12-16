from distutils.core import setup

setup(
    name='python-varnish',
    version='0.1',
    long_description=open('README.rst').read(),
    description='Simple Python interface for the Varnish management port',
    author='Justin Quick',
    author_email='justquick@gmail.com',
    url='http://github.com/justquick/python-varnish',
    scripts=['bin/varnish_manager'],
    packages=['varnish'],
)
