import QtQuick 2.5

import DICE.App 1.0
import DICE.Components 1.0

Column {
    spacing: 10
    width: parent.width
    height: childrenRect.height

    DropDown2 {
        id: typeDropDown
        label: qsTr('Type')

        model: [
            "cyclic",
            "cyclicAMI",
        ] 
        path: "boundary:boundary_group_type"
    }
    DiceButton {
        width: parent.width
        text: 'Ungroup'
        onClicked: app.breakGroup()
    }

}