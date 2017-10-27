import QtQuick 2.5

import DICE.App 1.0

Column {
    width: parent.width
    height: childrenRect.height

    spacing: 20

    Subheader {
        text: "Type"
    }
    DiceComboBox {
        id: epsilonType
        model: ["Fixed Value",
                "Turbulent Mixing Length Inlet",
                "Zero Gradient", "Symmetry", "Slip"]
        path: "boundary:epsilon_boundary_condition_type"
    }

    DiceValueField {
        enabled: (["Fixed Value"]).indexOf(epsilonType.currentText) >= 0
        label: "Value [m^2/s^3]"
        path: "boundary:epsilon_field_value"
    }

    DiceValueField {
        enabled: (["Turbulent Mixing Length Inlet"
            ]).indexOf(epsilonType.currentText) >= 0
        label: "Mixing Length [m]"
        path: "boundary:epsilon_mixing_length_value"
    }
}
