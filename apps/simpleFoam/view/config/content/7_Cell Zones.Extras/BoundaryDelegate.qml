import QtQuick 2.9
import QtQuick.Layouts 1.3

import DICE.Components 1.0

Item {
    width: parent.width
    height: 20

    RowLayout {
        width: parent.width
        height: 20
        anchors.verticalCenter: parent.verticalCenter

        BasicText {
            Layout.fillWidth: true
            anchors.margins: 5
            anchors.verticalCenter: parent.verticalCenter
            text: name
        }
    }
}
