from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from zope.configuration import xmlconfig


class CollectiveBtreesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.btrees
        xmlconfig.file('configure.zcml', collective.btrees,
                      context=configurationContext)

COLLECTIVE_BTREES_FIXTURE = CollectiveBtreesLayer()
COLLECTIVE_BTREES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_BTREES_FIXTURE,), name="CollectiveBtrees:Integration")

# A few helper functions.


def make_test_doc(portal):
    new_id = portal.generateUniqueId('Document')
    portal.invokeFactory('Document', new_id)
    doc = portal[new_id]
    doc.reindexObject()  # Might have already happened, but let's be sure.
    return doc
