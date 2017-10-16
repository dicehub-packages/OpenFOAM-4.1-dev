import QtQuick 2.5

import DICE.App 1.0

Column {
    width: parent.width
    height: childrenRect.height

    spacing: 20
    
    VectorField {
        path: "refinement:SearchableSphere.centre"
        xLabel: "Centre X"
        yLabel: "Centre Y"
        zLabel: "Centre Z"
    }

    ValueField {
        path: "refinement:SearchableSphere.radius"
        width: parent.width/2
        label: "Radius [m]"
    }
}
