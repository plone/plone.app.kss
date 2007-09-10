
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
        kukit.log('KSS started by Plone DOMLoad event.');
        kukit.bootstrapFromDOMLoad();
    };
    addDOMLoadEvent(f);
;;; kukit.log('KSS bootstrap set up in Plone DOMLoad event.');
} else {
;;; var msg = 'Plone addDOMLoadEvent not found by KSS, DOMLoad activation';
;;; msg += ' skipped (you might want to add event-registration.js to ';
;;; msg += ' ResourceRegistries).';
;;; kukit.logWarning(msg);
}

/* Base kukit plugins for Plone*/

kukit.actionsGlobalRegistry.register("plone-initKupu", function(oper) {
    kukit.logDebug('Enter plone-initKupu');
    oper.evaluateParameters([], {}, 'plone-initKupu action');
    // we start from the iframe node...
    if (oper.node.tagName.toLowerCase() != 'iframe') {
;;;     kukit.E = 'The plone-initKupu action can only be setup on an iframe';
;;;     kukit.E += ' node.';
        throw kukit.E;
    }
    var divnode = oper.node.parentNode.parentNode.parentNode.parentNode;
    var id = divnode.id;
    if (! id) {
;;;     kukit.E = 'The plone-initKupu action did not find the editor id from';
;;;     kukit.E += ' the iframe node.';
        throw kukit.E;
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
                kukit.log('Setup Kupu initialization on load event.');
                var self = this;
                initKupuOnLoad = function() {
                    kukit.log('Initialize Kupu from onload event.');
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
kukit.commandsGlobalRegistry.registerFromAction('plone-initKupu', 
    kukit.cr.makeSelectorCommand);

kukit.actionsGlobalRegistry.register("plone-followLink", function(oper) {
    oper.evaluateParameters([], {}, 'plone-followLink action');
    var url = oper.node.href;
    if (url.substr(0, 7) == "http://") {
        // redirect to it
        window.location.replace(url);
    } else if (url.substr(0, 13) == "javascript://") {
        // execute it
        eval(url.substr(13));
    }
});
kukit.commandsGlobalRegistry.registerFromAction('plone-followLink',
    kukit.cr.makeSelectorCommand);

kukit.actionsGlobalRegistry.register("plone-submitCurrentForm", function (oper) {
    oper.evaluateParameters([], {}, 'plone-submitCurrentForm action');
    // disable the onbeforeunload event since we want to submit now.
    window.onbeforeunload = null;
    var form = new kukit.fo.CurrentFormLocator(oper.node).getForm();
    form.submit();
});
kukit.commandsGlobalRegistry.registerFromAction('plone-submitCurrentForm',
    kukit.cr.makeSelectorCommand);

kukit.actionsGlobalRegistry.register("plone-initFormTabs", function(oper) {
    oper.evaluateParameters([], {}, 'plone-initFormTabs action');
    if (oper.node.tagName.toLowerCase() != 'form') {
;;;     kukit.E = 'The plone-initFormTabs action can only execute on a form';
;;;     kukit.E += ' node as a target.';
        throw kukit.E;
    }
    var form = oper.node;  
    ploneFormTabbing.initializeForm(form);
});
kukit.commandsGlobalRegistry.registerFromAction('plone-initFormTabs', kukit.cr.makeSelectorCommand);

kukit.actionsGlobalRegistry.register("plone-initFormProtection", function(oper) {
    oper.evaluateParameters([], {}, 'plone-initFormProtection action');
    if (oper.node.tagName.toLowerCase() != 'form') {
;;;     kukit.E = 'The plone-initFormProtection action can only execute on';
;;;     kukit.E += ' a form node as a target.';
        throw kukit.E;
    }
    var form = oper.node;  
    if (! window.onbeforeunload) {
        window.onbeforeunload = new BeforeUnloadHandler().execute;
    }
    var tool = window.onbeforeunload.tool;
    // We add the new tool to the 
    tool.addForm(form);
});
kukit.commandsGlobalRegistry.registerFromAction('plone-initFormProtection',
    kukit.cr.makeSelectorCommand);

kukit.actionsGlobalRegistry.register("plone-formProtectionCheck", 
    function(oper) {
    oper.evaluateParameters([], {}, 'plone-formProtectionCheck action');
    // Find the binderInstance of the switcher.
    // (since we are in an action and not in the event,
    // we don't have it at hand.
    // Note that we would not necessarily need the singleton)
    var binderInfo =
        kukit.engine.binderInfoRegistry.getSingletonBinderInfoByName('plone',
        'formProtectionChecked');
    var binderInstance = binderInfo.getBinderInstance();
    // check if the form has change
    var message;
    if ( window.onbeforeunload) {
        var tool = window.onbeforeunload.tool;
        message = tool.execute();
    }
    // Do we need the popup?
    var result = true;
    if (message) {
        var confirmMsg = 'Are you sure you want to navigate away from this';
        confirmMsg += ' page?\n\n' + message + '\n\nPress OK to continue,';
        confirmMsg += ' or Cancel to stay on the current page.';
        result = confirm(confirmMsg);
    }
    // arrange the continuation events
    if (result) {
        // Continue with the real action.
        var action = 'formProtectionChecked';
    } else {
        // Continue with the cancel action.
        var action = 'formProtectionFailed';
    }
    binderInstance.__continueEvent__(action, oper.node, {});
});

kukit.commandsGlobalRegistry.registerFromAction('plone-formProtectionCheck',
    kukit.cr.makeSelectorCommand);

kukit.plone.FormProtectionCheckedEvents = function() {
};

kukit.plone.FormProtectionCheckedEvents.prototype.__default_failed__ = 
    function(name, oper) {
};

kukit.eventsGlobalRegistry.register('plone', 'formProtectionChecked',
    kukit.plone.FormProtectionCheckedEvents, null, null);

kukit.eventsGlobalRegistry.register('plone', 'formProtectionFailed',
    kukit.plone.FormProtectionCheckedEvents, null, '__default_failed__');

// Form Locking

kukit.actionsGlobalRegistry.register("plone-initLockingProtection",
    function(oper) {
    oper.evaluateParameters([], {}, 'plone-initLockingProtection action');
    if (oper.node.tagName.toLowerCase() != 'form') {
;;;     kukit.E = 'The plone-initLockingProtection action can only execute';
;;;     kukit.E += ' on a form node as a target.';
        throw kukit.E;
    }
    if (! window.onunload) {
        var handler = new plone.UnlockHandler().execute;
        window.onunload = handler;
    }
});
kukit.commandsGlobalRegistry.registerFromAction('plone-initLockingProtection',
    kukit.cr.makeSelectorCommand);


kukit.actionsGlobalRegistry.register("plone-removeLockProtection",
    function(oper) {
    oper.evaluateParameters([], {}, 'plone-removeLockProtection action');
    if ( window.onunload) {
        window.onunload = null;
    }
});
kukit.commandsGlobalRegistry.registerFromAction('plone-removeLockProtection',
    kukit.cr.makeGlobalCommand);

// Folder contents shift click selection
kukit.actionsGlobalRegistry.register("plone-initShiftDetection",
    function(oper) {
    oper.evaluateParameters([], {}, 'plone-initShiftDetection action');

    kukit.engine.stateVariables['plone-shiftdown'] = false;
    document.onkeydown = function(e) {
        var evt = e || window.event;
        if(evt.keyCode == 16){
            kukit.engine.stateVariables['plone-shiftdown'] = true;
        }
    };

    document.onkeyup = function(e) {
        var evt = e || window.event;
        if(evt.keyCode == 16){
            kukit.engine.stateVariables['plone-shiftdown'] = false;
        }
    };
});
kukit.commandsGlobalRegistry.registerFromAction('plone-initShiftDetection',
    kukit.cr.makeSelectorCommand);


kukit.actionsGlobalRegistry.register("plone-initCheckBoxSelection",
    function(oper) {
    oper.evaluateParameters([], {}, 'plone-initCheckBoxSelection action');
    kukit.engine.stateVariables['plone-foldercontents-firstcheckeditem'] = null;
});
kukit.commandsGlobalRegistry.registerFromAction('plone-initCheckBoxSelection',
    kukit.cr.makeSelectorCommand);


kukit.actionsGlobalRegistry.register("plone-createCheckBoxSelection",
    function(oper) {
    var actionMsg = 'plone-createCheckBoxSelection action';
    oper.evaluateParameters(['group'], {}, actionMsg);

    var node = oper.node;
    var firstItemVarName = 'plone-foldercontents-firstcheckeditem';
    var firstItem = kukit.engine.stateVariables[firstItemVarName];
    if(firstItem && kukit.engine.stateVariables['plone-shiftdown']) {
        var group = oper.parms.group;
        var allNodes = kukit.dom.cssQuery(group);
        var start = null;
        var end = null;
        for(var i=0; i < allNodes.length; i++){
            if(allNodes[i] == firstItem){
                start = i;
            }
            else if(allNodes[i] == node){
                end = i;
            }
        }
        if(start>end){
            var temp = start;
            start = end;
            end = temp;
        }

        for(var i=start; i <= end; i++){
            allNodes[i].checked = firstItem.checked;
        }
    }
    else {
        kukit.engine.stateVariables[firstItemVarName] = node;
    }
});
kukit.commandsGlobalRegistry.registerFromAction('plone-createCheckBoxSelection',
    kukit.cr.makeSelectorCommand);


kukit.actionsGlobalRegistry.register("plone-initDragAndDrop",
    function(oper) {
    oper.evaluateParameters(['table'], {}, 'plone-initDragAndDrop action');
    var table = oper.parms.table;
    ploneDnDReorder.table = cssQuery(table)[0];
    if (!ploneDnDReorder.table)
        return;
    ploneDnDReorder.rows = cssQuery(table + " > tr," +
                                    table + " > tbody > tr");
    var targets = cssQuery(table + " > tr > td.draggable," +
                           table + " > tbody > tr > td.draggable");
    for (var i=0; i<targets.length; i++) {
        if (hasClassName(targets[i], 'notDraggable'))
            continue;
	var target = targets[i];
        target.onmousedown=ploneDnDReorder.doDown;
        target.onmouseup=ploneDnDReorder.doUp;
        addClassName(target, "draggingHook");
	target.innerHTML = '::'
    }
});
kukit.commandsGlobalRegistry.registerFromAction('plone-initDragAndDrop',
    kukit.cr.makeSelectorCommand);
