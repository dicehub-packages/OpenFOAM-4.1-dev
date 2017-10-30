import QtQuick 2.9
import QtQuick.Layouts 1.3

import DICE.Components 1.0


Item {
    height: 20
    
    Connections {
        target: delegateRoot
        onDoubleClicked: showInScene()
    }

    RowLayout {
        width: parent.width
        height: 20
        anchors.verticalCenter: parent.verticalCenter

        Item {
            Layout.minimumWidth: 20
            height: 20
            anchors.verticalCenter: parent.verticalCenter
            FontAwesomeIcon {
                size: 12
                anchors.centerIn: parent
                name: {
                    return "File";
                }
            }
        }

        BasicText {
            Layout.fillWidth: true
            anchors.margins: 5
            anchors.verticalCenter: parent.verticalCenter
            text: label + " " + boundaryType + " " + boundaryOrientation
        }

        MouseArea {
            Layout.minimumWidth: 20
            height: 20
            anchors.verticalCenter: parent.verticalCenter
            enabled: type === "RefinementObject"
            visible: enabled

            FontAwesomeIcon {
                size: 12
                anchors.centerIn: parent
                name: "Remove"
            }
            onClicked: {
                remove()
            }
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
                name: isVisible ? "Eye" : "EyeSlash"
            }
            onClicked: {
                isVisible = ! isVisible
            }
        }

    }
}
