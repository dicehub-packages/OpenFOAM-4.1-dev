import QtQuick 2.5

import DICE.App 1.0
//import DICE.Components 1.0

Column {
    width: parent.width
    height: childrenRect.height

    spacing: 20

    Subheader {
        text: "Type"
    }
    DiceComboBox {
        id: pressureType
        model: ["Fixed Value", "Total Pressure", "Zero Gradient", "Slip", "Symmetry"]
        path: "boundary:pressure_boundary_condition_type"
    }
    DiceValueField {
        enabled: (["Fixed Value", "Total Pressure"]).indexOf(pressureType.currentText) >= 0
        visible: enabled
        label: "Pressure [Pa]"
        path: "boundary:pressure_field_value"
    }
}
