from Products.Five import BrowserView
import logging
from Products.Archetypes.utils import addStatusMessage

logger=logging.getLogger('kss')

# objects_tree defines the tree of kss contents used in our tests
# You can add your objects used in kss tests and generic attributes
objects_tree = [{'id':'kssfolder', 
                 'portal_type':'Folder',
                 'attrs':{
                          'title':'KssFolder',
                          'description':'Folder for KSS contents',
                         },
                 'children':[{'id':'documentitem',
                              'portal_type':'Document',
                              'children':[],
                              'attrs':{
                                       'title':'KssDocument',
                                       'text':"""
                                              KSS is a javascript framework that aims to allow Ajax development 
                                              without javascript. It uses stylesheets with CSS-compliant syntax 
                                              to setup behaviours in the client and a set of well-defined commands 
                                              that are marshalled back from the server to manipulate the DOM.
                                              We'll also add an external link also (<a href="http://www.plone.org">
                                              [bug #6343] click here to test if the external link works!</a>).
                                              """,
                                       'description':"""
                                                     KSS is a javascript framework that aims to allow Ajax development 
                                                     without javascript.
                                                     """,
                                      }
                             },
                             {'id':'newsitem',
                              'portal_type':'News Item',
                              'children':[],
                              'attrs':{
                                       'title':'KssNews',
                                       'text':"""
                                              An early spring sprint at a beautiful location on the Italian coast. 
                                              The sprint will focus on topics of interest for Plone 3.5. Potential 
                                              topics include custom membership, extending Plone's use of AJAX, 
                                              content export-import, and much more.
                                              """,
                                       'description':"""
                                                     Sorrento sprint
                                                     """,
                                      }
                             },
                            ]
                }]

class SiteCreationView(BrowserView):
  
  def createNodes(self, node=None, objs_tree=[]):
      """ Recursive method that create the tree structure of content types used for kss tests """
      for item in objs_tree:
          obj_id = item.get('id')
          obj_pt = item.get('portal_type')
          obj_attrs = item.get('attrs')
          obj_children = item.get('children')
          if hasattr(node, obj_id):
              # if the object exists, we'll delete it
              node.manage_delObjects([obj_id])
          node.invokeFactory(obj_pt, obj_id)
          new_obj = getattr(node, obj_id, None)
          # writing object attributes
          new_obj.update(**obj_attrs)
          
          # recursive call for creating other nodes
          self.createNodes(new_obj, obj_children)

  def createSite(self):
      """ This method invokes the recursive method createNodes which creates the tree structure of
          objects used by """
      context = self.context
      self.createNodes(context, objects_tree)

      status_message='Selenium Test Site has been created'
      logger.info(status_message)

      url = context.absolute_url()
      addStatusMessage(context.REQUEST, status_message)
      context.request.RESPONSE.redirect(url)
