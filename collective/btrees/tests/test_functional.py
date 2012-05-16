import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from collective.btrees.testing import (
    COLLECTIVE_BTREES_INTEGRATION_TESTING,
    make_test_doc,
    )


class TestCollectiveBtrees(unittest.TestCase):

    layer = COLLECTIVE_BTREES_INTEGRATION_TESTING

    def _makeOne(self):
        return make_test_doc(self.layer['portal'])

    def testItems_keys_values_and_iterators(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        doc = self._makeOne()
        from collective.btrees.interfaces import IOOBTreeContainer
        container = IOOBTreeContainer(doc)
        self.assertEqual(len(container.keys()), 0)
        key = object()
        value = object()
        container.insert(key, value)
        self.assertEqual(container.get(key), value)
        self.assertEqual(len(container.items()), 1)
        self.assertEqual(len(container.keys()), 1)
        self.assertEqual(len(container.values()), 1)
        self.assertEqual(list(container.items()), [(key, value)])
        self.assertEqual(list(container.keys()), [key])
        self.assertEqual(list(container.values()), [value])

        # Test the iterators.
        item_iterator = container.iteritems()
        self.assertEqual(item_iterator.next(), (key, value))
        self.assertRaises(StopIteration, item_iterator.next)
        key_iterator = container.iterkeys()
        self.assertEqual(key_iterator.next(), key)
        self.assertRaises(StopIteration, key_iterator.next)
        value_iterator = container.itervalues()
        self.assertEqual(value_iterator.next(), value)
        self.assertRaises(StopIteration, value_iterator.next)

    def testGetNonExisting(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        doc = self._makeOne()
        from collective.btrees.interfaces import IOOBTreeContainer
        container = IOOBTreeContainer(doc)
        # Getting a non-existing item.
        self.assertEqual(container.get('foobar'), None)
        self.assertEqual(container.get('foobar', 'ni'), 'ni')
        self.assertEqual(container.pop('none'), None)
        self.assertEqual(container.pop('none', 'hi'), 'hi')

    def testPopItem(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        doc = self._makeOne()
        from collective.btrees.interfaces import IOOBTreeContainer
        container = IOOBTreeContainer(doc)
        # Insert an item and pop it.
        key = object()
        value = object()
        container.insert(key, value)
        self.assertEqual(len(container.items()), 1)
        self.assertEqual(container.pop(key), value)
        self.assertEqual(len(container.items()), 0)
        self.assertEqual(container.pop(key), None)

    def testClear(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        doc = self._makeOne()
        from collective.btrees.interfaces import IOOBTreeContainer
        container = IOOBTreeContainer(doc)
        container.insert(object(), object())
        container.insert(object(), object())
        container.insert(object(), object())
        self.assertEqual(len(container.items()), 3)
        # Remove all.
        container.clear()
        self.assertEqual(len(container.items()), 0)
        self.assertEqual(len(container.keys()), 0)
        self.assertEqual(len(container.values()), 0)
        self.assertRaises(StopIteration, container.iteritems().next)
        self.assertRaises(StopIteration, container.iterkeys().next)
        self.assertRaises(StopIteration, container.itervalues().next)
        # Clearing an empty container should work too of course.
        container.clear()

    def testMinimumMaximum(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        from collective.btrees.interfaces import IIOBTreeContainer
        doc = self._makeOne()
        container = IIOBTreeContainer(doc)
        self.assertEqual(len(container.keys()), 0)
        container.insert(1, 'one')
        container.insert(2, 'two')
        container.insert(3, 'three')
        container.insert(4, 'four')
        container.insert(5, 'five')
        self.assertEqual(container.get(1), 'one')
        self.assertEqual(len(container.items()), 5)
        self.assertEqual(len(container.keys()), 5)
        self.assertEqual(len(container.values()), 5)
        self.assertEqual(list(container.keys(min=4)), [4, 5])
        self.assertEqual(list(container.keys(max=2)), [1, 2])
        self.assertEqual(list(container.keys(min=2, max=4)), [2, 3, 4])

    def testSetdefault(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        doc = self._makeOne()
        from collective.btrees.interfaces import IOOBTreeContainer
        container = IOOBTreeContainer(doc)
        key = object()
        first = object()
        second = object()
        self.assertEqual(container.get(key), None)
        self.assertEqual(container.setdefault(key, first), first)
        self.assertEqual(container.get(key), first)
        self.assertEqual(container.setdefault(key, second), first)
        self.assertEqual(container.get(key), first)

    def testUpdate(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        doc = self._makeOne()
        from collective.btrees.interfaces import IOOBTreeContainer
        container = IOOBTreeContainer(doc)
        key1 = object()
        key2 = object()
        value1 = object()
        value2 = object()
        container.update({key1: value1, key2: value2})
        self.assertEqual(container.get(key1), value1)
        self.assertEqual(container.get(key2), value2)
        # Turn it around.
        container.update({key1: value2, key2: value1})
        self.assertEqual(container.get(key1), value2)
        self.assertEqual(container.get(key2), value1)

    def testIFBTree(self):
        try:
            from BTrees.IFBTree import IFBTree
            IFBTree  # pyflakes
        except ImportError:
            # Does not exist yet in Plone 3.
            return
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        doc = self._makeOne()
        from collective.btrees.interfaces import IIFBTreeContainer
        container = IIFBTreeContainer(doc)
        self.assertEqual(len(container.keys()), 0)
        key = 1
        value = 1.2
        self.assertEqual(container.get(key), None)
        container.insert(key, value)
        # With floats there can be slight differences.
        self.assertAlmostEqual(container.get(key), value)
        self.assertEqual(list(container.keys()), [key])
        self.assertEqual(len(container.values()), 1)
        self.assertAlmostEqual(container.values()[0], value)
        container.clear()
        self.assertEqual(list(container.keys()), [])

    def testIIBTree(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        doc = self._makeOne()
        from collective.btrees.interfaces import IIIBTreeContainer
        container = IIIBTreeContainer(doc)
        self.assertEqual(len(container.keys()), 0)
        key = 1
        value = 2
        self.assertEqual(container.get(key), None)
        container.insert(key, value)
        self.assertEqual(container.get(key), value)
        self.assertEqual(list(container.items()), [(key, value)])
        container.clear()
        self.assertEqual(list(container.keys()), [])

    def testIOBTree(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        doc = self._makeOne()
        from collective.btrees.interfaces import IIOBTreeContainer
        container = IIOBTreeContainer(doc)
        self.assertEqual(len(container.keys()), 0)
        key = 1
        value = object()
        self.assertEqual(container.get(key), None)
        container.insert(key, value)
        self.assertEqual(container.get(key), value)
        self.assertEqual(list(container.items()), [(key, value)])
        container.clear()
        self.assertEqual(list(container.keys()), [])

    def testLFBTree(self):
        try:
            from BTrees.LFBTree import LFBTree
            LFBTree  # pyflakes
        except ImportError:
            # Does not exist yet in Plone 3.
            return
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        doc = self._makeOne()
        from collective.btrees.interfaces import ILFBTreeContainer
        container = ILFBTreeContainer(doc)
        self.assertEqual(len(container.keys()), 0)
        key = long(1)
        value = 1.2
        self.assertEqual(container.get(key), None)
        container.insert(key, value)
        # With floats there can be slight differences.
        self.assertAlmostEqual(container.get(key), value)
        self.assertEqual(list(container.keys()), [key])
        self.assertEqual(len(container.values()), 1)
        self.assertAlmostEqual(container.values()[0], value)
        container.clear()
        self.assertEqual(list(container.keys()), [])

    def testLLBTree(self):
        try:
            from BTrees.LLBTree import LLBTree
            LLBTree  # pyflakes
        except ImportError:
            # Does not exist yet in Plone 3.
            return
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        doc = self._makeOne()
        from collective.btrees.interfaces import ILLBTreeContainer
        container = ILLBTreeContainer(doc)
        self.assertEqual(len(container.keys()), 0)
        key = long(1)
        value = long(2)
        self.assertEqual(container.get(key), None)
        container.insert(key, value)
        self.assertEqual(container.get(key), value)
        self.assertEqual(list(container.items()), [(key, value)])
        container.clear()
        self.assertEqual(list(container.keys()), [])

    def testLOBTree(self):
        try:
            from BTrees.LOBTree import LOBTree
            LOBTree  # pyflakes
        except ImportError:
            # Does not exist yet in Plone 3.
            return
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        doc = self._makeOne()
        from collective.btrees.interfaces import ILOBTreeContainer
        container = ILOBTreeContainer(doc)
        self.assertEqual(len(container.keys()), 0)
        key = long(1)
        value = object()
        self.assertEqual(container.get(key), None)
        container.insert(key, value)
        self.assertEqual(container.get(key), value)
        self.assertEqual(list(container.items()), [(key, value)])
        container.clear()
        self.assertEqual(list(container.keys()), [])

    def testOIBTree(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        doc = self._makeOne()
        from collective.btrees.interfaces import IOIBTreeContainer
        container = IOIBTreeContainer(doc)
        self.assertEqual(len(container.keys()), 0)
        key = object()
        value = 1
        self.assertEqual(container.get(key), None)
        container.insert(key, value)
        self.assertEqual(container.get(key), value)
        self.assertEqual(list(container.items()), [(key, value)])
        container.clear()
        self.assertEqual(list(container.keys()), [])

    def testOLBTree(self):
        try:
            from BTrees.OLBTree import OLBTree
            OLBTree  # pyflakes
        except ImportError:
            # Does not exist yet in Plone 3.
            return
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        doc = self._makeOne()
        from collective.btrees.interfaces import IOLBTreeContainer
        container = IOLBTreeContainer(doc)
        self.assertEqual(len(container.keys()), 0)
        key = object()
        value = long(1)
        self.assertEqual(container.get(key), None)
        container.insert(key, value)
        self.assertEqual(container.get(key), value)
        self.assertEqual(list(container.items()), [(key, value)])
        container.clear()
        self.assertEqual(list(container.keys()), [])

    def testOOBTree(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        doc = self._makeOne()
        from collective.btrees.interfaces import IOOBTreeContainer
        container = IOOBTreeContainer(doc)
        self.assertEqual(len(container.keys()), 0)
        key = object()
        value = object()
        self.assertEqual(container.get(key), None)
        container.insert(key, value)
        self.assertEqual(container.get(key), value)
        self.assertEqual(list(container.items()), [(key, value)])
        container.clear()
        self.assertEqual(list(container.keys()), [])
