from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase import PloneTestCase as ptc
from kss.core.tests.base import KSSLayer, KssViewTestCase

class KSSAndPloneLayer(PloneSite, KSSLayer):
    pass

class KSSAndPloneTestCase(ptc.PloneTestCase, KssViewTestCase):
    layer = KSSAndPloneLayer
