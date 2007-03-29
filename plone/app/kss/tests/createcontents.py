request = container.REQUEST
RESPONSE =  request.RESPONSE

context.invokeFactory('Folder', id='kssFolder', title='KssFolder', description='Folder for KSS test contents')
folder = getattr(context, 'AzaxFolder')

document_body = 'KSS is a javascript framework that aims to allow Ajax development without javascript. It uses stylesheets with      CSS-compliant syntax to setup behaviours in the client and a set of well-defined commands that are marshalled back from the server to manipulate the DOM.'

document_description ='KSS is a javascript framework that aims to allow Ajax development without javascript.'

folder.invokeFactory('Document', id='azaxDocument', title='Kss', description=document_description, text=document_body)

