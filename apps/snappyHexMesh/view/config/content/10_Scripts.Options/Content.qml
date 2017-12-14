import QtQuick 2.5
import DICE.App 1.0
import QtQuick.Layouts 1.3

Body {
    id: root

    property var codeEditorPopup

    Component.onCompleted: {
        var newComponent = Qt.createComponent("CodeEditorPopup.qml");
        if (newComponent.status === Component.Ready) {
            root.codeEditorPopup = newComponent.createObject(appWindow, {});
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
                root.codeEditorPopup.openScript('initialization.py')
            }
        }

        DiceButton {
            width: parent.width
            text: qsTr("Pre-run")
            onClicked: {
                root.codeEditorPopup.openScript('pre_run.py')
            }
        }

        DiceButton {
            width: parent.width
            text: qsTr("Post-run")
            onClicked: {
                root.codeEditorPopup.openScript('post_run.py')
            }
        }
    }
}
