import QtQuick 2.4
import QtWebEngine 1.5
import QtQuick.Layouts 1.3
import DICE.Components 1.0
import DICE.App 1.0

WebEngineView {
    id: codeView

    Layout.fillHeight: true
    Layout.fillWidth: true

    settings.localContentCanAccessFileUrls: true
    settings.errorPageEnabled: true

    Connections {
        target: app
        onSaveRequest: {
            codeView.runJavaScript("editor.getValue()", function(result) { app.save(result); });
        } 
    }

    Component.onCompleted: {
        loadHtml('\
            <!DOCTYPE html>\
            <html>\
            <head>\
                <link rel="stylesheet" href="lib/codemirror.css">\
                <link rel="stylesheet" href="theme/elegant.css"> \
                <link rel="stylesheet" href="theme/monokai.css"> \
                <style media="screen" type="text/css">\
                    html { height:100%; width: 100%; }\
                    body { position:absolute; top:0; bottom:0; right:0; left:0; margin: 0; }\
                    .CodeMirror { height: 100%; width: 100%; }\
                </style>\
            </head>\
            <body>\
            <script src="lib/codemirror.js"></script>\
            <script src="mode/python/python.js"></script>\
            <script>\
                var editor = CodeMirror(document.body, {\
                    lineNumbers: true,\
                    readOnly: false,\
                    lineWrapping: false,\
                    mode: "python",\
                    theme: "monokai",\
                    value: '+JSON.stringify(app.script)+',\
                    });\
            </script>\
            </body>\
            </html>\
        ', Qt.resolvedUrl('CodeMirror/'));
    }
}
