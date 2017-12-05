import QtQuick 2.9

import DICE.App 1.0

Column {
    width: parent.width
    height: childrenRect.height

    spacing: 20

    DiceInlineComboBox {
        id: kType
        label: "Type"
        model: ["Fixed Value",
                "Turbulent Intensity Kinetic Energy Inlet",
                "Zero Gradient", "Symmetry", "Slip", "kqRWallFunction"]
        path: "boundary:k_boundary_condition_type"
    }

    DiceValueField {
        enabled: (["Fixed Value"]).indexOf(kType.currentText) >= 0
        label: "Value [J/kg]"
        path: "boundary:k_field_value"
    }

    DiceValueField {
        enabled: (["Turbulent Intensity Kinetic Energy Inlet"
            ]).indexOf(kType.currentText) >= 0
        label: "Intensity"
        path: "boundary:k_intensity_value"
    }
}
