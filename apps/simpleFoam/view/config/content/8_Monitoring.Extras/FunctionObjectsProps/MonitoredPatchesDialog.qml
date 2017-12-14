import QtQuick 2.9
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.0

import DICE.App 1.0
import DICE.Components 1.0 as DC


DC.DiceDialog {
    id: root
    title: "Select Monitored Patches"

    property string objectPath: ""

    parent: appWindow.overlay

    x: Math.round((appWindow.width - width) / 2)
    y: Math.round(appWindow.height / 6)
    width: Math.round(Math.min(appWindow.width, appWindow.height) / 3 * 2)
    modal: true
    focus: true

    DiceValueConnector {
        id: patchesValueConnector
        path: root.objectPath + ".patches_model"
    }

    contentItem: Column {
        width: parent.width
        height: parent.height

        RowLayout {
            width: parent.width
            height: childrenRect.height

            Subheader {
               text: "Patches"
               Layout.fillWidth: true
               horizontalAlignment: "AlignHCenter"
            }
            Item {
                width: 50
                height: parent.height
            }
            Subheader {
                text: "Monitored Patches"
                Layout.fillWidth: true
                horizontalAlignment: "AlignHCenter"
            }
        }
        RowLayout {
            width: parent.width
            height: childrenRect.height

            SimpleTreeView {
                id: boundaries
                Layout.fillWidth: true
                height: parent.height
                model: app.boundariesModel
                delegate: SimpleTreeViewDelegate {
                    contentSource: 'BoundaryDelegate.qml'
                }
            }

            Rectangle {
                width: 50
                Layout.preferredWidth: 50
                height: parent.height
                color: "transparent"

                Column {
                    width: parent.width

                    DiceIconButton {
                        iconName: "AngleRight"
                        anchors.horizontalCenter: parent.horizontalCenter
                        onClicked: app.functionObjects.call('add_patches')
                        enabled: canAddPatches.value
                        DiceValueConnector {
                            id: canAddPatches
                            path: root.objectPath + ".can_add_patches"
                        }
                    }
                    DiceIconButton {
                        iconName: "AngleLeft"
                        anchors.horizontalCenter: parent.horizontalCenter
                        onClicked: app.functionObjects.call('remove_patches')
                        enabled: canRemovePatches.value
                        DiceValueConnector {
                            id: canRemovePatches
                            path: root.objectPath + ".can_remove_patches"
                        }
                    }
                }
            }

            SimpleTreeView {
                id: monitoredPatches
                Layout.fillWidth: true
                model: patchesValueConnector.value
                delegate: SimpleTreeViewDelegate {
                    contentSource: 'BoundaryDelegate.qml'
                }
            }
        }

        Row {
            width: parent.width
            spacing: 10

            Item {
                width: parent.width/2 - spacing/2
                height: parent.height
            }
            Button {
                id: confirmButton

                width: parent.width/2 - spacing/2
                text: qsTr("Close")
                onClicked: {
                    root.accept()
                }
            }
        }
    }
    Keys.onReturnPressed: {
        confirmButton.clicked()
    }
    Keys.onEscapePressed: {
        cancelButton.clicked()
    }
}
