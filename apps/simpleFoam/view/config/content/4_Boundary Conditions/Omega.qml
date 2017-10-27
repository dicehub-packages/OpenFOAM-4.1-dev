import QtQuick 2.5

import DICE.App 1.0
//import DICE.Components 1.0

Column {
    width: parent.width
    height: childrenRect.height

    spacing: 20

    Subheader {
        text: "Type"
    }
    DiceComboBox {
        id: omegaType
        model: ["Fixed Value",
                "Turbulent Mixing Length Frequency Inlet",
                "Zero Gradient", "Symmetry"]
        path: "boundary:omega_boundary_condition_type"
    }

    DiceValueField {
        enabled: (["Fixed Value"]).indexOf(omegaType.currentText) >= 0
        label: "Value [1/s]"
        path: "boundary:omega_field_value"
    }

    DiceValueField {
        enabled: (["Turbulent Mixing Length Frequency Inlet"
            ]).indexOf(omegaType.currentText) >= 0
        label: "Mixing Length [m]"
        path: "boundary:omega_mixing_length_value"
    }
}
