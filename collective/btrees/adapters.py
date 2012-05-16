import logging

from BTrees.OOBTree import OOBTree
from persistent import Persistent
from zope.annotation.interfaces import IAnnotations
from zope.app.container.contained import ObjectAddedEvent
from zope.app.container.contained import ObjectRemovedEvent
from zope.event import notify
from zope.interface import Interface
from zope.interface import implements

logger = logging.getLogger('collective.btrees')


class IBTreeContainer(Interface):
    pass


class BTreeContainer(Persistent):

    implements(IBTreeContainer)
    ANNO_KEY = 'collective.btrees'

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(self.context)
        self.__mapping = annotations.get(self.ANNO_KEY, None)
        if self.__mapping is None:
            self.__mapping = OOBTree()  # XXX
            annotations[self.ANNO_KEY] = self.__mapping

    def _check_key(self, key):
        """Check if this key is valid.

        All keys in a btree should be of the same type.  At least cmp
        on keys should function properly, otherwise the btree will
        start acting basically randomly.  So if you fear this may not
        be the case, you can specify a check here.

        It does not return anything.  Must raise an exception
        (suggested is a ValueError) when the value is wrong.  Override
        this when you need a real check.
        """
        pass

    def _check_value(self, value):
        """Check if this value is valid.

        It does not return anything.  Must raise an exception
        (suggested is a ValueError) when the value is wrong.  Override
        this when you need a real check.
        """
        pass

    def clear(self):
        return self.__mapping.clear()

    def get(self, key, default=None):
        return self.__mapping.get(key, default=default)

    def insert(self, key, value):
        self._check_key(key)
        self._check_value(value)
        result = self.__mapping.insert(key, value)
        event = ObjectAddedEvent(value, newParent=self.context, newName=key)
        notify(event)
        return result

    def items(self, min=None, max=None):
        return self.__mapping.items(min=min, max=max)

    def iteritems(self, min=None, max=None):
        return self.__mapping.iteritems(min=min, max=max)

    def iterkeys(self, min=None, max=None):
        return self.__mapping.iterkeys(min=min, max=max)

    def itervalues(self, min=None, max=None):
        return self.__mapping.itervalues(min=min, max=max)

    def keys(self, min=None, max=None):
        return self.__mapping.keys(min=min, max=max)

    def pop(self, k, d=None):
        _marker = object()
        result = self.__mapping.pop(k, d=_marker)
        if result is _marker:
            return d
        event = ObjectRemovedEvent(result, oldParent=self.context, oldName=k)
        notify(event)
        return result

    def setdefault(self, k, d):
        return self.__mapping.setdefault(k, d)

    def update(self, collection):
        return self.__mapping.update(collection)

    def values(self, min=None, max=None):
        return self.__mapping.values(min=min, max=max)
