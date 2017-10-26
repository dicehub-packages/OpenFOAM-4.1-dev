import QtQuick 2.9

import DICE.App 1.0

Column {
    width: parent.width
    height: childrenRect.height
    
    Row {
        spacing: 10
        width: parent.width

        ValueConnector {
            id: levelMode
            path: "refinement:RegionLevel.region_mode"
        }

        DiceVectorField2D2 {
            xLabel: "Distance [m]"
            yLabel: "Level"
            xDataType: "double"
            xEnabled: levelMode.value === "distance"
            yDataType: "int"
            path: "refinement:RegionLevel.data"
        }
    }
}
