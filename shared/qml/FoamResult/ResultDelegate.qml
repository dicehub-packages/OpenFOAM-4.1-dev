import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.3

import DICE.App 1.0
import DICE.Components 1.0

Item {
    width: parent.width
    height: 20
    RowLayout {

        Connections {
            target: delegateRoot
            onDoubleClicked: boundaryName.forceActiveFocus()
        }

        width: parent.width
        height: 20
        anchors.verticalCenter: parent.verticalCenter

        TextInput {
            id: boundaryName

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
        	visible: !boundaryName.focus
            Layout.fillWidth: true
            anchors.margins: 5
            anchors.verticalCenter: parent.verticalCenter
            text: name
        }

        MouseArea {
            Layout.minimumWidth: 20
            height: 20
            anchors.verticalCenter: parent.verticalCenter
            enabled: isVisible !== undefined
            visible: enabled
            FontAwesomeIcon {
                size: 12
                anchors.centerIn: parent
                name: isVisible ? "EyeOpen" : "EyeClose"
            }
            onClicked: {
                isVisible =! isVisible
            }
        }
    }
}