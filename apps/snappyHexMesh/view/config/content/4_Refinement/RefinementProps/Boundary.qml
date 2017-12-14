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
    }
    DiceComboBox {
        label: "Type"
        width: parent.width
        path: "refinement:Boundary.type"
        modelPath: "refinement:Boundary.boundary_types_model"
    }
}
