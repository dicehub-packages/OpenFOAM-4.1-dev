import QtQuick 2.9

import DICE.App 1.0

Column {
    width: parent.width
    height: childrenRect.height
    spacing: 20
    
    DiceVectorField {
        path: "refinement:SearchableSphere.centre"
        xLabel: "Centre X"
        yLabel: "Centre Y"
        zLabel: "Centre Z"
    }

    DiceValueField {
        path: "refinement:SearchableSphere.radius"
        width: parent.width/2
        label: "Radius [m]"
    }
}
