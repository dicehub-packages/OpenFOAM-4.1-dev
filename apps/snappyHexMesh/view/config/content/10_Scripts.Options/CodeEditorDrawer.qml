import DICE.App 1.0
import DICE.Components 1.0 as DC

import QtQuick.Layouts 1.1
import QtQuick 2.7
import QtWebEngine 1.3
import QtQuick.Controls 2.2

Popup {
    id: root

    width: 0.5 * appWindow.width
    height: 0.5 * appWindow.height
    x: 0.5 * (parent.width - width)
    y: 0.5 *(parent.height - height)

    modal: true
    focus: true

    property string scriptName

    function openScript(name) {
        root.scriptName = name;
        app.getScript(name, function (result) {
            codeView.runJavaScript("editor.setValue("+JSON.stringify(result)+")");
            root.open();
        })
    }

    onClosed: {
        codeView.runJavaScript("editor.getValue()", function(result) { app.saveScript(root.scriptName, result); });
    }

    ColumnLayout {

        anchors.fill: parent

        WebEngineView {
            id: codeView

            property bool ready: false

            Layout.fillHeight: true
            Layout.fillWidth: true

            settings.localContentCanAccessFileUrls: true
            settings.errorPageEnabled: true

            onLoadingChanged: {
                if (loadRequest.status == WebEngineView.LoadSucceededStatus) {
                    ready = true;
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
                            });\
                    </script>\
                    </body>\
                    </html>\
                ', Qt.resolvedUrl('CodeMirror/'));
                ready = true;
            }
        }

    }



}
