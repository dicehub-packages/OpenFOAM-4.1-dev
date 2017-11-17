import QtQuick 2.9

import DICE.App 1.0


Column {
    spacing: 10
    width: parent.width
    height: childrenRect.height

    Subheader {
        text: "Forces Monitor Settings"
        horizontalAlignment: "AlignHCenter"
    }

    Subheader {
        text: "Centre of rotation"
    }
    DiceVectorField {
        path: "functionObjects:ForcesMonitor.cofr"
    }

    Subheader {
        text: "Pitch axis"
    }
    DiceVectorField {
        path: "functionObjects:ForcesMonitor.pitch_axis"
    }

    DiceValueField {
        label: "Density [kg/m³]"
        path: "functionObjects:ForcesMonitor.rho_inf"
    }
}
