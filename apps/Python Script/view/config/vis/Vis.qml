import QtQuick 2.4
import QtWebEngine 1.5
import QtQuick.Layouts 1.3
import DICE.Components 1.0
import DICE.App 1.0

Item {
    Layout.fillHeight: true
    Layout.fillWidth: true

    WebEngineView {
        id: codeView

        anchors.fill: parent

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
        ', Qt.resolvedUrl('ace/'));
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
