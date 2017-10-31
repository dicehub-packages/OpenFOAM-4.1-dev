import QtQuick 2.9

import DICE.App 1.0

Column {
    width: parent.width
    height: childrenRect.height
    spacing: 20

    Subheader {
        text: "Base Point"
    }
    DiceVectorField {
        path: "refinement:SearchablePlanePaN.basePoint"
    }
    Subheader {
        text: "Normal Vector"
    }
    DiceVectorField {
        path: "refinement:SearchablePlanePaN.normal"
    }
}
