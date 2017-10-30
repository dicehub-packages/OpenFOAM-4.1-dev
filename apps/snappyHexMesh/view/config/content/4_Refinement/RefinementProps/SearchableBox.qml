import QtQuick 2.9

import DICE.App 1.0

Column {
    width: parent.width
    height: childrenRect.height
    spacing: 20

    DiceVectorField {
        path: "refinement:SearchableBox.min"
        xLabel: "minX"
        yLabel: "minY"
        zLabel: "minZ"
    }
    
    DiceVectorField {
        path: "refinement:SearchableBox.max"
        xLabel: "maxX"
        yLabel: "maxY"
        zLabel: "maxZ"
    }
}
