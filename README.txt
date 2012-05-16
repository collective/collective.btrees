.. contents::


Documentation
=============


Target audience
---------------

This is a package for integrators.

 
Installation and goal
---------------------

Add collective.btrees to the eggs in your buildout.  Add it to the
zcml too, if you are on Plone 3.2 or lower.  No need for further
installation in the Plone UI.

This makes some small adapters available to store btrees in
annotations on an object.  There are adapters for all the btrees in
the ``BTrees`` module.  The adapters make the public methods of btrees
available in the adapter.  Use this when you want this and when you
understand what this means. :-)


Example usage
-------------

Usually you will want to create an own adapter to override some
settings, at least the key used to store the annotations.  Put this in
an adapters.py::

  from zope.interface import implements
  from zope.interface import Interface
  from collective.btrees.interfaces import IOOBTreeContainer
  from collective.btrees.adapters import OOBTreeContainer

  class IFormValuesContainer(IOOBTreeContainer):
      pass

  class FormValuesContainer(OOBTreeContainer):

      implements(IFormValuesContainer)
      ANNO_KEY = 'my.package.formvalues'

      def _check_key(self, key):
          if not isinstance(key, basestring):
              raise TypeError("base string expected as key")

      def _check_value(self, value):
          if not isinstance(value, dict):
              raise TypeError("dictionary expected as value")

Register the adapter in zcml::

  <adapter
      for="zope.interface.Interface"
      provides=".adapters.IFormValuesContainer"
      factory=".adapters.FormValuesContainer"
      />

Use it within for example a browser view to store the request form
dictionary in the btree (if this for some reason makes sense for your
website)::

  container = IFormValuesContainer(self.context)
  key = 'my key'  # maybe use the user id as key
  value = self.request.form
  container.insert(key, value)
  container.get(key)  # will return value


Compatibility
-------------

I have tried this on Plone 3.3 and 4.1.  It will likely work on other versions
as well.


Authors
-------

Maurits van Rees
