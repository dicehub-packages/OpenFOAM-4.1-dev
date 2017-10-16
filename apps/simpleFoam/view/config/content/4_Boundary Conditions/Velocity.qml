import QtQuick 2.5

import DICE.App 1.0
import DICE.Components 1.0

Column {
    width: parent.width
    height: childrenRect.height
    
    spacing: 20

    DropDown2 {
        id: velocityType
        label: "Type"
        model: ["Fixed Value", "Zero Gradient", "Inlet Outlet", "Slip"]
        path: "boundary:velocity_boundary_condition_type"
    }

    VectorField {
        enabled: (["Fixed Value"]).indexOf(velocityType.currentText) >= 0
        visible: enabled
        xLabel: "Velocity X"
        yLabel: "Velocity Y"
        zLabel: "Velocity Z"
        path: "boundary:velocity_field_value"
    }

    VectorField {
        enabled: (["Inlet Outlet"]).indexOf(velocityType.currentText) >= 0
        visible: enabled
        xLabel: "Velocity X"
        yLabel: "Velocity Y"
        zLabel: "Velocity Z"
        path: "boundary:velocity_inlet_value"
    }

}
