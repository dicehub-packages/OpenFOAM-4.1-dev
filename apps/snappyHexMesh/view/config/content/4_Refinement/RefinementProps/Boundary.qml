import QtQuick 2.9

import DICE.App 1.0

Column {
    spacing: 10
    width: parent.width
    height: childrenRect.height
    
    DiceInputField {
        width: parent.width
        label: qsTr('Name')
        path: "refinement:Boundary.name"
        floating: false
    }

    DiceComboBox {
        width: parent.width
        path: "refinement:Boundary.type"
        model: ListModel {
            ListElement { text: qsTr("patch") }
            ListElement { text: qsTr("wall") }
            ListElement { text: qsTr("symmetryPlane") }
            ListElement { text: qsTr("symmetry") }
            ListElement { text: qsTr("empty") }
            ListElement { text: qsTr("wedge") }
            ListElement { text: qsTr("cyclic") }
            ListElement { text: qsTr("cyclicAMI") }
        }
    }
}
