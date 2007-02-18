
/* Use onDOMLoad event to initialize kukit
   earlier then the document is fully loaded,
   but after the DOM is at its place already.

   This functionality is missing from Plone 2.1,
   the script is present in >=2.5, but it is not
   always added to RR - it needs to be added manually.

   If it's present we use it.
*/

kukit.plone = {};

if (typeof(addDOMLoadEvent) != 'undefined') {
    var f = function() {
        kukit.log('Init triggered by the DOMLoad event of KSS for Plone');
        kukit.bootstrap();
    };
    addDOMLoadEvent(f);
    kukit.log('Installed DOMLoad event for KSS for Plone.');
} else {
    kukit.logWarning('addDOMLoadEvent is not found in KSS for Plone, skipping DOMLoad activation (add event-registration.js to ResourceRegistries?)');
}

/* Base kukit plugins for Plone*/

kukit.actionsGlobalRegistry.register("plone-initKupu", function(oper) {
    oper.completeParms([], {}, 'plone-initKupu action');
    // we start from the iframe node...
    if (oper.node.tagName.toLowerCase() != 'iframe') {
        throw 'The plone-initKupu action can only execute on the iframe node as a target.';
    }
    var divnode = oper.node.parentNode.parentNode.parentNode.parentNode;
    var id = divnode.id;
    if (! id) {
        throw 'The plone-initKupu action did not find the editor id from the iframe node.';
    }
 
    //
    // Register the editor to ourselves
    // This makes possible to execute update on the field
    //
    var prefix = '#'+id+' ';
    var textarea = getFromSelector(prefix+'textarea.kupu-editor-textarea');
    kukit.fo.fieldUpdateRegistry.register(textarea,
            {editor: null,
             node: textarea,
             doInit: function() {
                this.editor = initPloneKupu(id);
                },
             doUpdate: function() {
                this.editor.saveDataToField(this.node.form, this.node);
                // set back _initialized
                // XXX check if this is actually ok?
                this.editor._initialized = true;
                }
             });
});
kukit.commandsGlobalRegistry.registerFromAction('plone-initKupu', kukit.cr.makeSelectorCommand);

kukit.actionsGlobalRegistry.register("plone-followLink", function(oper) {
    oper.completeParms([], {}, 'plone-followLink action');
    var url = oper.node.href;
    if (url.substr(0, 7) == "http://") {
        // redirect to it
        window.location.replace(url);
    } else if (url.substr(0, 13) == "javascript://") {
        // execute it
        eval(url.substr(13));
    }
});
kukit.commandsGlobalRegistry.registerFromAction('plone-followLink', kukit.cr.makeSelectorCommand);

kukit.actionsGlobalRegistry.register("plone-submitCurrentForm", function (oper) {
    oper.completeParms([], {}, 'plone-submitCurrentForm action');
    var form = kukit.fo.getCurrentForm(oper.node);
    form.submit();
});
kukit.commandsGlobalRegistry.registerFromAction('plone-submitCurrentForm', kukit.cr.makeSelectorCommand);

kukit.actionsGlobalRegistry.register("plone-initFormTabs", function(oper) {
    oper.completeParms([], {}, 'plone-initFormTabs action');
    if (oper.node.tagName.toLowerCase() != 'form') {
        throw 'The plone-initFormTabs action can only execute on a form node as a target.';
    }
    var form = oper.node;  
    ploneFormTabbing.initializeForm(form);
});
kukit.commandsGlobalRegistry.registerFromAction('plone-initFormTabs', kukit.cr.makeSelectorCommand);
 

kukit.actionsGlobalRegistry.register("toggleClassOnParent", function (oper) {
    oper.completeParms(['parenttype', 'value'], {}, 'toggleClassOnParent action');

    var node = oper.node;

    var parenttype = oper.parms.parenttype.toUpperCase();
    var value = oper.parms.value;

    var parentnode = node.parentNode;
    while(parentnode.parentNode) {
        if(parentnode.nodeName.toUpperCase()==parenttype){
            break;
        }
        parentnode = parentnode.parentNode;
    }
    var nodeclass = kukit.dom.getAttribute(parentnode, 'class');
    var foundclassatindex = -1;
    var parts = nodeclass.split(' ');
    for(var i=0; i<parts.length; i++){
        if(parts[i]==value){
            foundclassatindex = i;
        }
    }
    if(foundclassatindex==-1){
        parts.push(value);
    } else {
        parts.splice(foundclassatindex, 1);
    }
    kukit.dom.setAttribute(parentnode, 'class', parts.join(' '));
});
kukit.commandsGlobalRegistry.registerFromAction('toggleClassOnParent', kukit.cr.makeGlobalCommand);
