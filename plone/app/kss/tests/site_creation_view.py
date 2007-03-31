from Products.Five import BrowserView
import logging
logger=logging.getLogger('kss')

class SiteCreationView(BrowserView):
  
  def createSite(self):
      context = self.context
      context.invokeFactory('Folder', id='folderitem', title='KssFolder', description='Folder for KSS contents')
      folder = getattr(context, 'folderitem')

      document_body = """KSS is a javascript framework that aims to allow Ajax development without javascript. 
                         It uses stylesheets with CSS-compliant syntax to setup behaviours in the client and a set of 
                         well-defined commands that are marshalled back from the server to manipulate the DOM.
                         We'll also add an external link also (<a href="http://www.plone.org">[bug #6343] click here 
                         to test if the external link works!</a>).
                         """
      document_description ='KSS is a javascript framework that aims to allow Ajax development without javascript.'

      folder.invokeFactory('Document', id='documentitem', title='Kss', description=document_description, text=document_body)

      news_description = 'Sorrento sprint'
      news_body = "An early spring sprint at a beautiful location on the Italian coast. The sprint will focus on topics of interest for Plone 3.5. Potential topics include custom membership, extending Plone's use of AJAX, content export-import, and much more."
      folder.invokeFactory('News Item', id='newsitem', title='KssNews', description=news_description, text=news_body)
      logger.info('Site created for Selenium Test')
      return('OK: Site created for Selenium Test')
