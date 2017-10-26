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
        model: ["Fixed Value", "Zero Gradient"]
        path: "boundary:velocity_boundary_condition_type"
    }

    DiceVectorField2 {
        enabled: (["Fixed Value"]).indexOf(velocityType.currentText) >= 0
        xLabel: "Velocity X"
        yLabel: "Velocity Y"
        zLabel: "Velocity Z"
        path: "boundary:velocity_field_value"
    }
}
