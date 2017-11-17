import QtQuick 2.9

import DICE.App 1.0


Column {
    spacing: 10
    width: parent.width
    height: childrenRect.height

    Subheader {
        text: "Force coefficients Monitor Settings"
        horizontalAlignment: "AlignHCenter"
    }

    Subheader {
        text: "Centre of rotation"
    }
    DiceVectorField {
        path: "functionObjects:ForceCoeffsMonitor.cofr"
    }

    Subheader {
        text: "Pitch axis"
    }
    DiceVectorField {
        path: "functionObjects:ForceCoeffsMonitor.pitch_axis"
    }

    Subheader {
        text: "Drag direction"
    }
    DiceVectorField {
        path: "functionObjects:ForceCoeffsMonitor.drag_dir"
    }

    Subheader {
        text:  "Lift direction"
    }
    DiceVectorField {
        path: "functionObjects:ForceCoeffsMonitor.lift_dir"
    }

    DiceValueField {
        label: "Density [kg/m³]"
        path: "functionObjects:ForceCoeffsMonitor.rho_inf"
    }

    DiceValueField {
        label: "Reference area [m²]"
        path: "functionObjects:ForceCoeffsMonitor.a_ref"
    }
    DiceValueField {
        label: "Reference length [m]"
        path: "functionObjects:ForceCoeffsMonitor.l_ref"
    }
    DiceValueField {
        label: "Reference area [m²]"
        path: "functionObjects:ForceCoeffsMonitor.a_ref"
    }
    DiceValueField {
        label: "Freestream velocity magnitude [m/s]"
        path: "functionObjects:ForceCoeffsMonitor.mag_u_inf"
    }
}
