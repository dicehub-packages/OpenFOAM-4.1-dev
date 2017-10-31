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
        path: "refinement:SearchablePlane3P.point1"
    }
    Subheader {
        text: "Point 2"
    }
    DiceVectorField {
        path: "refinement:SearchablePlane3P.point2"
    }
    Subheader {
        text: "Point 3"
    }
    DiceVectorField {
        path: "refinement:SearchablePlane3P.point3"
    }
}
