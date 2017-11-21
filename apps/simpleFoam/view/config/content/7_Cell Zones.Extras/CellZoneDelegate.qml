import QtQuick 2.9
import QtQuick.Layouts 1.3

import DICE.Components 1.0

Item {
    width: parent.width
    height: Math.max(25, buttonLabel.height + 20)


    RowLayout {
        width: parent.width
        height: 20
        anchors.verticalCenter: parent.verticalCenter

        Item {
            Layout.minimumWidth: 20
            height: 20
            anchors.verticalCenter: parent.verticalCenter
            property Component fileIcon: DiceFontAwesomeIcon {
                size: 12
                anchors.centerIn: parent
                name: "Folder"
            }
            Loader {
                anchors.centerIn: parent
                sourceComponent: parent.fileIcon
            }
        }

        BasicText {
            id: buttonLabel
            Layout.fillWidth: true
            anchors.margins: 5
            anchors.verticalCenter: parent.verticalCenter
            text: name
        }
    }
}
