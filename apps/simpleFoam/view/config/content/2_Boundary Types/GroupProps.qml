import QtQuick 2.9

import DICE.App 1.0

Column {
    spacing: 10
    width: parent.width
    height: childrenRect.height

    Subheader {
        text: "Type"
    }
    DiceComboBox {
        id: typeDropDown
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
