try:
    from Products.Five import BrowserView
    BrowserView = BrowserView   # satisfy pyflakes
except ImportError:
    from zope.publisher.browser import BrowserView

from Acquisition import aq_parent
from OFS.interfaces import IApplication
from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import setSecurityManager, newSecurityManager

class SetupBase(BrowserView):
    """This class provides the basic bootstrap set for every
    test suite bootstrapping. You must inherit from this class
    and override just the run method"""

    _required_role = 'Manager'

    def __init__(self, context, request):
        super(SetupBase, self).__init__(context, request)
        #go up to the root
        parent = aq_parent(self.context.aq_inner)
        while not IApplication.providedBy(parent):
            try:
                parent = parent.aq_parent
            except AttributeError:
                break
        self.zoperoot = [parent]

    def checkPermission(self, zoperoot):
        # The form must be submitted by POST, and authenticate correctly.
        method = self.request.get("REQUEST_METHOD", "GET").upper()
        username = self.request.get("username", None)
        password = self.request.get("password", None)
        if method == "POST" and username is not None and password is not None:
            admin = zoperoot.acl_users.authenticate(username, password, None)
            if self._required_role in admin.getRoles():
                return admin
        return None
    
    def run(self, zoperoot):
        """Just override me"""
        raise Exception("Functionality not implemented")

    def start(self):
        zoperoot = self.zoperoot[0]
        user = self.checkPermission(zoperoot)
        if user is not None:
            old_sm = getSecurityManager()
            wrapped_user = user.__of__(zoperoot.acl_users)
            newSecurityManager(self.request, wrapped_user)
            result = self.run(zoperoot)
            setSecurityManager(old_sm)
            return result
        else:
            raise Exception("You are trying to run potentially disruptive code without providing a good auth")

    __call__ = start
