import QtQuick 2.9

import DICE.App 1.0


Column {
    DiceValueField {
        label: "Pressure [Pa]"
        visible: modelData.modelData === "Pressure"
        path: "foam:0/p internalField %field"
    }
    DiceVectorField {
        xLabel: "Ux [m/s]"
        yLabel: "Uy [m/s]"
        zLabel: "Uz [m/s]"
        visible: modelData.modelData === "Velocity"
        path: "foam:0/U internalField %field_vector"
    }
    DiceValueField {
        label: "Turbulent kinetic energy [m²/s²]"
        visible: modelData.modelData === "k"
        path: "foam:0/k internalField %field"
    }
    DiceValueField {
        label: "Turbulence specific dissipation rate"
        visible: modelData.modelData === "Omega"
        path: "foam:0/omega internalField %field"
    }
    DiceValueField {
        label: "Turbulence dissipation rate [m²/s³]"
        visible: modelData.modelData === "Epsilon"
        path: "foam:0/epsilon internalField %field"
    }
    DiceValueField {
        label: "Turbulence viscosity [m²/s]"
        visible: modelData.modelData === "nut"
        path: "foam:0/nut internalField %field"
    }
    DiceSwitch {
        id: initializationWithPotentialFoamSwitch
        text: qsTr("Initialize with potentialFoam")
        path: "config:potentialFoam"
    }
    DiceInlineSpinBox {
        enabled: initializationWithPotentialFoamSwitch.checked
        visible: enabled
        label: "Non Orthogonal Correctors (potentialFoam)"
        path: "foam:system/fvSolution potentialFlow nNonOrthogonalCorrectors"
    }
}
