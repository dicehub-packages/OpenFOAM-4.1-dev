import QtQuick 2.9
import QtQuick.Layouts 1.3

import DICE.Components 1.0

Item {
    width: parent.width
    height: {
        if (functionObjectName.visible)
            return functionObjectName.height
        else
            return Math.max(25, buttonLabel.height + 20)
    }

    RowLayout {
        width: parent.width
        height: 20
        anchors.verticalCenter: parent.verticalCenter

        Connections {
            target: delegateRoot
            onDoubleClicked: functionObjectName.forceActiveFocus()
        }

        RowLayout {
            id: col

            spacing: 2
            anchors.verticalCenter: parent.verticalCenter

            DiceTextField {
                id: functionObjectName

                Layout.fillWidth: true
                anchors.margins: 5
                visible: focus
                text: name
                anchors.verticalCenter: parent.verticalCenter
                activeFocusOnPress: false
                onFocusChanged: {
                    if (!focus) {
                        name=text
                    }
                }
                onEditingFinished: {
                    focus = false
                }
            }

            BasicText {
                id: buttonLabel
                Layout.fillWidth: true
                verticalAlignment: Text.AlignVCenter
                anchors {
                    left: parent.left
                    leftMargin: 10
                    rightMargin: 10
                }
                text: label
                font.bold: selected
                color: colors.theme["text_color"]
                visible: !functionObjectName.focus
            }

            MouseArea {
                Layout.minimumWidth: 20
                height: 20
                anchors.verticalCenter: parent.verticalCenter
                enabled: type == "TreeNode"
                visible: enabled
                cursorShape: "PointingHandCursor"
                hoverEnabled: true

                DiceFontAwesomeIcon {
                    size: 12
                    anchors.centerIn: parent
                    name: "Plus"
                }
                onClicked: {
                    app.functionObjects.addFunctionObject(nodeType)
                }

                DiceToolTip {
                    text: "Add Function"
                    visible: parent.containsMouse
                    delay: 500
                }
            }
            MouseArea {
                Layout.minimumWidth: 20
                height: 20
                anchors.verticalCenter: parent.verticalCenter
                enabled: type !== "TreeNode"
                visible: enabled
                cursorShape: "PointingHandCursor"
                hoverEnabled: true

                DiceFontAwesomeIcon {
                    size: 10
                    anchors.centerIn: parent
                    name: "Remove"
                    color: colors.theme["text_color_info"]
                }
                onClicked: {
                    remove()
                }
                DiceToolTip {
                    text: "Remove Function"
                    visible: parent.containsMouse
                    delay: 500
                }
            }
        }
    }
}
