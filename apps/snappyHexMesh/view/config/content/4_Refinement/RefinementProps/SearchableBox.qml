import QtQuick 2.5

import DICE.App 1.0

Column {
    width: parent.width
    height: childrenRect.height
    
    VectorField {
        path: "refinement:SearchableBox.min"
        xLabel: "minX"
        yLabel: "minY"
        zLabel: "minZ"
    }
    
    VectorField {
        path: "refinement:SearchableBox.max"
        xLabel: "maxX"
        yLabel: "maxY"
        zLabel: "maxZ"
    }
}
