import QtQuick 2.9

import DICE.App 1.0
import DICE.Components 1.0 as DC

Column {
    spacing: 10
    width: parent.width
    height: childrenRect.height

    DiceSwitch {
        text: "Active"
        checked: active
        onClicked: {
            active = !active
        }
    }
}
