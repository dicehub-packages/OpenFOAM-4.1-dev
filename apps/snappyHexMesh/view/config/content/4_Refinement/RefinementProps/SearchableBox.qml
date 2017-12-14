import QtQuick 2.9

import DICE.App 1.0

Column {
    width: parent.width
    height: childrenRect.height
    spacing: 20

    DiceVectorField {
        path: "refinement:SearchableBox.min"
        xLabel: "min_X"
        yLabel: "min_Y"
        zLabel: "min_Z"
    }
    
    DiceVectorField {
        path: "refinement:SearchableBox.max"
        xLabel: "max_X"
        yLabel: "max_Y"
        zLabel: "max_Z"
    }
}
