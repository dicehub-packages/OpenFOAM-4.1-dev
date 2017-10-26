import QtQuick 2.5

import DICE.App 1.0

Column {
    width: parent.width
    height: childrenRect.height
    
    spacing: 20

    Subheader {
        text: "Type"
    }
    DiceComboBox {
        id: velocityType
        model: ["Fixed Value", "Zero Gradient", "Inlet Outlet", "Slip"]
        path: "boundary:velocity_boundary_condition_type"
    }

    DiceVectorField {
        enabled: (["Fixed Value"]).indexOf(velocityType.currentText) >= 0
        visible: enabled
        xLabel: "Velocity X"
        yLabel: "Velocity Y"
        zLabel: "Velocity Z"
        path: "boundary:velocity_field_value"
    }

    DiceVectorField {
        enabled: (["Inlet Outlet"]).indexOf(velocityType.currentText) >= 0
        visible: enabled
        xLabel: "Velocity X"
        yLabel: "Velocity Y"
        zLabel: "Velocity Z"
        path: "boundary:velocity_inlet_value"
    }

}
