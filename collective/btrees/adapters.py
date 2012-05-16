import logging

import BTrees
from persistent import Persistent
from zope.annotation.interfaces import IAnnotations
from zope.app.container.contained import ObjectAddedEvent
from zope.app.container.contained import ObjectRemovedEvent
from zope.event import notify
from zope.interface import implements

from collective.btrees import interfaces

logger = logging.getLogger('collective.btrees')


class BaseBTreeContainer(object):

    implements(interfaces.IBaseTreeContainer)
    ANNO_KEY = 'collective.btrees'
    btree_class = None

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(self.context)
        self.__mapping = annotations.get(self.ANNO_KEY, None)
        if self.__mapping is None:
            self.__mapping = self.btree_class()
            annotations[self.ANNO_KEY] = self.__mapping

    def _check_key(self, key):
        """Check if this key is valid.

        All keys in a btree should be of the same type.  At least cmp
        on keys should function properly, otherwise the btree will
        start acting basically randomly.  So if you fear this may not
        be the case, you can specify a check here.

        It does not return anything.  Must raise an exception
        (suggested is a TypeError) when the key is wrong.  Override
        this when you need a real check.
        """
        pass

    def _check_value(self, value):
        """Check if this value is valid.

        It does not return anything.  Must raise an exception
        (suggested is a TypeError) when the value is wrong.  Override
        this when you need a real check.
        """
        pass

    def clear(self):
        return self.__mapping.clear()

    def get(self, key, default=None):
        return self.__mapping.get(key, default)

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
        result = self.__mapping.pop(k, _marker)
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


class IFBTreeContainer(BaseBTreeContainer):

    implements(interfaces.IIFBTreeContainer)
    ANNO_KEY = 'collective.btrees.ifbtree'
    btree_class = BTrees.IFBTree.IFBTree


class IIBTreeContainer(BaseBTreeContainer):

    implements(interfaces.IIIBTreeContainer)
    ANNO_KEY = 'collective.btrees.iibtree'
    btree_class = BTrees.IIBTree.IIBTree


class IOBTreeContainer(BaseBTreeContainer):

    implements(interfaces.IIOBTreeContainer)
    ANNO_KEY = 'collective.btrees.iobtree'
    btree_class = BTrees.IOBTree.IOBTree


class LFBTreeContainer(BaseBTreeContainer):

    implements(interfaces.ILFBTreeContainer)
    ANNO_KEY = 'collective.btrees.lfbtree'
    btree_class = BTrees.LFBTree.LFBTree


class LLBTreeContainer(BaseBTreeContainer):

    implements(interfaces.ILLBTreeContainer)
    ANNO_KEY = 'collective.btrees.llbtree'
    btree_class = BTrees.LLBTree.LLBTree


class LOBTreeContainer(BaseBTreeContainer):

    implements(interfaces.ILOBTreeContainer)
    ANNO_KEY = 'collective.btrees.lobtree'
    btree_class = BTrees.LOBTree.LOBTree


class OIBTreeContainer(BaseBTreeContainer):

    implements(interfaces.IOIBTreeContainer)
    ANNO_KEY = 'collective.btrees.oibtree'
    btree_class = BTrees.OIBTree.OIBTree


class OLBTreeContainer(BaseBTreeContainer):

    implements(interfaces.IOLBTreeContainer)
    ANNO_KEY = 'collective.btrees.olbtree'
    btree_class = BTrees.OLBTree.OLBTree


class OOBTreeContainer(BaseBTreeContainer):

    implements(interfaces.IOOBTreeContainer)
    ANNO_KEY = 'collective.btrees.oobtree'
    btree_class = BTrees.OOBTree.OOBTree
