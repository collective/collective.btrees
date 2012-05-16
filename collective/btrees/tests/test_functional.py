import unittest2 as unittest

#from plone.app.testing import setRoles

from collective.btrees.testing import (
    COLLECTIVE_BTREES_INTEGRATION_TESTING,
    make_test_doc,
    )


class TestCollectiveBtrees(unittest.TestCase):

    layer = COLLECTIVE_BTREES_INTEGRATION_TESTING

    def _makeOne(self):
        return make_test_doc(self.layer['portal'])

    def testSomething(self):
        self.assertEqual(1, 2)
