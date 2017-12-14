import QtQuick 2.9

import DICE.App 1.0

Column {
    width: parent.width
    height: childrenRect.height
    spacing: 20
    
    Subheader {
        text: "Point 1"
    }

    DiceVectorField {
        path: "refinement:SearchableCylinder.point_1"
    }

    Subheader {
        text: "Point 2"
    }

    DiceVectorField {
        path: "refinement:SearchableCylinder.point_2"
    }

    DiceValueField {
        path: "refinement:SearchableCylinder.radius"
        width: parent.width/2
        label: "Radius [m]"
    }
}
