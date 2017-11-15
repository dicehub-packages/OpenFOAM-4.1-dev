import QtQuick 2.9
import QtQuick.Layouts 1.1

import DICE.App 1.0


Column {
    spacing: 10
    width: parent.width
    height: childrenRect.height

    DiceButton {
        text: "ShowProps"
        onClicked: app.monitoring.showProps()
    }
}
