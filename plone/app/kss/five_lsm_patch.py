import Acquisition
from zope.component.interfaces import ComponentLookupError
import zope.component.persistentregistry
import five.localsitemanager.registry
import OFS.ObjectManager
import logging
logger = logging.getLogger('plone.app.kss')

_marker = object()

# XXX monkeypatching zope
# this will make sure, if our utility provides the marker, we will
# provide the necessary parameters to it
class PatchComponent(object):

    def queryUtility(self, provided, name=u'', default=None):
        utility = self.utilities.lookup((), provided, name, default)
        if utility is not default:
            utility = self._wrap(utility)
        return utility

    def getUtility(self, provided, name=u''):
        utility = self.queryUtility(provided, name=name, default=_marker)
        if utility is _marker:
            raise ComponentLookupError(provided, name)
        return utility

    def getUtilitiesFor(self, interface):
        for name, utility in self.utilities.lookupAll((), interface):
            utility = self._wrap(utility)
            yield name, utility

    def _wrap(self, comp):
        """Return an aq wrapped component with the site as the parent but
        only if the comp has an aq wrapper to begin with.
        """

        # BBB: The primary reason for doing this sort of wrapping of
        # returned utilities is to support CMF tool-like functionality where
        # a tool expects it's aq_parent to be the portal object.  New code
        # (ie new utilities) should not rely on this predictability to
        # get the portal object and should search out an alternate means
        # (possibly retrieve the ISiteRoot utility).  Although in most
        # cases getting at the portal object shouldn't be the required pattern
        # but instead looking up required functionality via other (possibly
        # local) components.

        if Acquisition.interfaces.IAcquirer.providedBy(comp): 

            # sitemanager contains the sitemamager that the caller called
            # the query on. Howewer this is not necessarily the same sitemanager
            # on which this regisrty is on. We need to iterate on all site managers
            # and figure out which ones we are.
            sitemanager = self._select_sm()
            if sitemanager is None:
                # no sm provides acquisition
                return comp

            parent = sitemanager.aq_parent
            base = Acquisition.aq_base(comp)

            if base is not Acquisition.aq_base(parent):
                # If the component is not the component registry container,
                # wrap it in the parent
                comp = base.__of__(parent)
            else:
                # If the component happens to be the component registry
                # container we are looking up a ISiteRoot.
                # We are not wrapping it in itself but in its own parent
                comp = base.__of__(Acquisition.aq_parent(parent))

        return comp

    def _iter_all_sitemanagers(self, sitemanager):
        yield sitemanager
        for chained_sm in sitemanager.__bases__:
            for more in self._iter_all_sitemanagers(chained_sm):
                yield more

    def _select_sm(self):
        '''Select the correct site manager

        choose one from the site managers, that have acquisition info

        We should actually return the sitemanager that has the registry
        But unfortunately, we cannot know _which_ sitemanager is giving us
        the registry, so the first one that has aq wrapping, will be used
        XXX and this is totally wrong in fact.
        '''
        for sm in self._iter_all_sitemanagers(self):
            if Acquisition.aq_parent(sm) is not None:
                break
        else:
            # Site manager not found (no aq info, sorry)
            sm = None
        return sm

# apply the monkeypatches
import zope.component.registry
for key in PatchComponent.__dict__.iterkeys():
    if not key.startswith('__'):
        setattr(zope.component.registry.Components, key,
                getattr(PatchComponent, key).im_func)
logger.info('*** monkeypatching zope.component.registry.Components ***')

# XXX Now we need to patch five.localsitamanager too.
# Because the acquisition is originally added from there, but since we have relocated
# this functionality to the z3 level, it will be applied for every site manager, so no
# reason to apply it also from Five's one.

def _init_registries(self):
    self.adapters = zope.component.persistentregistry.PersistentAdapterRegistry()
    self.utilities = zope.component.persistentregistry.PersistentAdapterRegistry()

for key in ('queryUtility', 'getUtility', 'getUtilitiesFor',
        'getAllUtilitiesRegisteredFor'):
    setattr(five.localsitemanager.registry.PersistentComponents, key,
            getattr(zope.component.persistentregistry.PersistentComponents, key))
five.localsitemanager.registry.PersistentComponents._init_registries = \
        _init_registries
logger.info('*** monkeypatching five.localsitemanager.registry.PersistentComponents ***')
