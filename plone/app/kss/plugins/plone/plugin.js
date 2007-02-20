
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
        kukit.log('KSS initialized by Plone DOMLoad event.');
        kukit.bootstrapFromDOMLoad();
    };
    addDOMLoadEvent(f);
    kukit.log('Installed KSS bootstrap in Plone DOMLoad event.');
} else {
    kukit.logWarning('Plone addDOMLoadEvent not found by KSS, DOMLoad activation skipped (you might want to add event-registration.js to ResourceRegistries)');
}

/* Base kukit plugins for Plone*/

kukit.actionsGlobalRegistry.register("plone-initKupu", function(oper) {
    kukit.logDebug('Enter plone-initKupu');
    oper.completeParms([], {}, 'plone-initKupu action');
    // we start from the iframe node...
    if (oper.node.tagName.toLowerCase() != 'iframe') {
        throw 'The plone-initKupu action can only be setup on an iframe node.';
    }
    var divnode = oper.node.parentNode.parentNode.parentNode.parentNode;
    var id = divnode.id;
    if (! id) {
        throw 'The plone-initKupu action did not find the editor id from the iframe node.';
    }
 
    //
    // Register the kupu editor in KSS
    // This enables KSS to update the textarea explicitely. 
    //
    var prefix = '#'+id+' ';
    var textarea = getFromSelector(prefix+'textarea.kupu-editor-textarea');
    kukit.fo.fieldUpdateRegistry.register(textarea,
            {editor: null,
             node: textarea,
             doInit: function() {
                kukit.log('Setup Kupu initialization on load event');
                var self = this;
                initKupuOnLoad = function() {
                    kukit.log('Initialize Kupu from onload event');
                    self.editor = initPloneKupu(id);
                };
                this.editor = initPloneKupu(id);
                registerEventListener(window, "load", initKupuOnLoad);
                },
             doUpdate: function() {
                this.editor.saveDataToField(this.node.form, this.node);
                // set back _initialized
                // XXX check if this is actually ok?
                this.editor._initialized = true;
                }
             });
    kukit.logDebug('plone-initKupu action done.');
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
    // disable the onbeforeunload event since we want to submit now.
    window.onbeforeunload = null;
    //
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

kukit.actionsGlobalRegistry.register("plone-initFormProtection", function(oper) {
    oper.completeParms([], {}, 'plone-initFormProtection action');
    if (oper.node.tagName.toLowerCase() != 'form') {
        throw 'The plone-initFormProtection action can only execute on a form node as a target.';
    }
    var form = oper.node;  
    if (! window.onbeforeunload) {
        window.onbeforeunload = new BeforeUnloadHandler().execute;
    }
    var tool = window.onbeforeunload.tool;
    // We add the new tool to the 
    tool.addForm(form);
});
kukit.commandsGlobalRegistry.registerFromAction('plone-initFormProtection', kukit.cr.makeSelectorCommand);

kukit.actionsGlobalRegistry.register("plone-formProtectionCheck", function(oper) {
    oper.completeParms([], {}, 'plone-formProtectionCheck action');
    // Find the binderinstance of the switcher.
    // (since we are in an action and not in the event, we don't have it at hand.
    // Note that we would not necessarily need the singleton)
    var binderinfo = kukit.engine.binderInfoRegistry.getSingletonBinderInfoByName('plone', 'formProtectionChecked');
    var binderinstance = binderinfo.getBinderInstance();
    if (true) {
        // Continue with the real action.
        binderinstance.__continue_event__('formProtectionChecked', oper.node, {});
    } else {
        binderinstance.__continue_event__('formProtectionFailed', oper.node, {});
    }
});
kukit.commandsGlobalRegistry.registerFromAction('plone-formProtectionCheck', kukit.cr.makeSelectorCommand);

kukit.plone.FormProtectionCheckedEvents = function() {
};
kukit.eventsGlobalRegistry.register('plone', 'formProtectionChecked', kukit.plone.FormProtectionCheckedEvents, null, null);
kukit.eventsGlobalRegistry.register('plone', 'formProtectionFailed', kukit.plone.FormProtectionCheckedEvents, null, null);


