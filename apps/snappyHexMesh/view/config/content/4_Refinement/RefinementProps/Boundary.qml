import QtQuick 2.5

import DICE.App 1.0
import DICE.Components 1.0

Column {
    spacing: 10
    width: parent.width
    height: childrenRect.height
    
    InputField2 {
        width: parent.width
        label: qsTr('Name')
        path: "refinement:Boundary.name"
        floating: false
    }

    DropDown2 {
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
            ListElement { text: qsTr("processor") }
        }
    }
}
