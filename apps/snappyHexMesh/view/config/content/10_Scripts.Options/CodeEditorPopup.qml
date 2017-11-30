import DICE.App 1.0
import DICE.Components 1.0 as DC

import QtQuick.Layouts 1.1
import QtQuick 2.7
import QtWebEngine 1.5
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

    Item {
        anchors.fill: parent

        WebEngineView {
            id: codeView

            property bool ready: false

            anchors.fill: parent

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
                      <meta charset="UTF-8">\
                      <style type="text/css" media="screen">\
                        #editor {\
                            position: absolute;\
                            top: 0;\
                            bottom: 0;\
                            left: 0;\
                            right: 0;\
                        }\
                      </style>\
                    </head>\
                    <body>\
                    <div id="editor">
                    </div>
                    <script src="src-min/ace.js" type="text/javascript" charset="utf-8"></script>\
                    <script>\
                        var editor = ace.edit("editor");\
                        editor.setTheme("ace/theme/monokai");\
                        editor.session.setMode("ace/mode/python");\
                        editor.setValue('+JSON.stringify(app.script)+', 1);\
                        editor.setShowPrintMargin(false);\
                    </script>\
                    </body>\
                    </html>\
                ', Qt.resolvedUrl('../../../../../../shared/common/ace/'));
            }
        }
        MouseArea {
            anchors.fill: parent
            acceptedButtons: Qt.NoButton
            propagateComposedEvents: true
            onWheel: {
                if (wheel.modifiers & Qt.ControlModifier) {
                    var angle = wheel.angleDelta.y
                    if (angle>0) {
                        codeView.zoomFactor += 0.1;
                    }
                    else {
                        codeView.zoomFactor -= 0.1;
                    }
                } else {
                    wheel.accepted = false;
                }
            }
        }
    }
}
