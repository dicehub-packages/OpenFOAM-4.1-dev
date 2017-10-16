import QtQuick 2.5

import DICE.Components 1.0
import DICE.App 1.0


Rectangle {
    color: "transparent"
    height: 35
    width: parent.width

    MenuText {
        text: "Your steps"
        anchors.centerIn: parent
    }
    BottomBorder {}
}
