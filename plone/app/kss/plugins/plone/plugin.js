
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
        kukit.initializeRules();
    };
    addDOMLoadEvent(f);
    kukit.log('Installed DOMLoad event for KSS for Plone.');
} else {
    kukit.logWarning('addDOMLoadEvent is not found in KSS for Plone, skipping DOMLoad activation (add event-registration.js to ResourceRegistries?)');
}

/* Base kukit plugins for Plone*/

kukit.ar.actionRegistry.register("plone-initKupu", function(oper) {
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
    window.kupu = initPloneKupu(id);
    //
    // Register the editor to ourselves
    // This makes possible to execute update on the field
    //
    var prefix = '#'+id+' ';
    //var iframe = getFromSelector(prefix+'iframe.kupu-editor-iframe');
    var textarea = getFromSelector(prefix+'textarea.kupu-editor-textarea');
    kukit.fo.fieldUpdateRegistry.register(textarea,
            {editor: window.kupu,
             node: textarea,
             doUpdate: function() {
                this.editor.saveDataToField(this.node.form, this.node);
                // set back _initialized
                // XXX check if this is actually ok?
                this.editor._initialized = true;
                }
             });
    // Finish setup
    window.kupuui = window.kupu.getTool('ui');
    window.drawertool = window.kupu.getTool('drawertool');
    window.kupu.initialize();
    //
    // We do some correction here. Problem: the kupu editor
    // initialization trasforms the original AT widget. It cannot
    // be called twice. If this happens, on IE a second hidden input
    // field for the text format qill appear and this will destruct
    // the traditional (non-ajax) form submit. Solution:
    //
    //  - we should not have a duplicate call of the editor init (we
    //    need to, currently, because the original inline init does not
    //    register the editor.
    //
    //  - in addition the initialize should not add the node for a second
    //    time, once added
    //
    var form = textarea.form;
    var elements = form.elements;
    var fmtname = textarea.name + '_text_format';
    var hiddencnt = 0;
    for (var y=0; y<elements.length; y++) {
        var element = elements[y];
        if (element.tagName.toLowerCase() == 'input' && element.name == fmtname) {
            if (hiddencnt > 0) {
                // delete all further duplicates
                element.parentNode.removeChild(element);
            }
            hiddencnt += 1;
        }
    }
});
kukit.cr.commandRegistry.registerFromAction('plone-initKupu', kukit.cr.makeSelectorCommand);

kukit.ar.actionRegistry.register("plone-followLink", function(oper) {
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
kukit.cr.commandRegistry.registerFromAction('plone-followLink', kukit.cr.makeSelectorCommand);

kukit.ar.actionRegistry.register("plone-submitCurrentForm", function (oper) {
    oper.completeParms([], {}, 'plone-submitCurrentForm action');
    var form = kukit.fo.getCurrentForm(oper.node);
    form.submit();
});
kukit.cr.commandRegistry.registerFromAction('plone-submitCurrentForm', kukit.cr.makeSelectorCommand);

kukit.ar.actionRegistry.register("plone-initFormTabs", function(oper) {
    oper.completeParms([], {}, 'plone-initFormTabs action');
    if (oper.node.tagName.toLowerCase() != 'form') {
        throw 'The plone-initFormTabs action can only execute on a form node as a target.';
    }
    var form = oper.node;  
    ploneFormTabbing.initializeForm(form);
});
kukit.cr.commandRegistry.registerFromAction('plone-initFormTabs', kukit.cr.makeSelectorCommand);
 
