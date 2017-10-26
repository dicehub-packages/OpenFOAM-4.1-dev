import QtQuick 2.5
import DICE.App 1.0
import QtQuick.Layouts 1.3

Body {
    id: root

    property var codeEditorDrawer

    Component.onCompleted: {
        var newComponent = Qt.createComponent("CodeEditorDrawer.qml");
        if (newComponent.status === Component.Ready) {
            root.codeEditorDrawer = newComponent.createObject(appWindow, {});
        } else if (newComponent.status === Component.Error) {
            console.error("Error creating Connector component:",
                          newComponent.errorString());
        }
    }

    Card {
        title: "Scripts"

        DiceButton {
            width: parent.width
            text: qsTr("Initialization")
            onClicked: {
                root.codeEditorDrawer.openScript('initialization.py')
            }
        }

        DiceButton {
            width: parent.width
            text: qsTr("Pre-run")
            onClicked: {
                root.codeEditorDrawer.openScript('pre_run.py')
            }
        }

        DiceButton {
            width: parent.width
            text: qsTr("Post-run")
            onClicked: {
                root.codeEditorDrawer.openScript('post_run.py')
            }
        }
    }
}
