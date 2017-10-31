import QtQuick 2.9

import DICE.App 1.0

Column {
    width: parent.width
    height: childrenRect.height
    spacing: 20

    Subheader {
        text: "Origin"
    }
    DiceVectorField {
        path: "refinement:SearchableDisk.origin"
    }
    Subheader {
        text: "Normal"
    }
    DiceVectorField {
        path: "refinement:SearchableDisk.normal"
    }
    DiceValueField {
        label: "Radius [m]"
        path: "refinement:SearchableDisk.radius"
    }
}
