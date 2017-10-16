import QtQuick 2.5

import DICE.App 1.0
import DICE.Components 1.0

Column {
    width: parent.width
    height: childrenRect.height

    spacing: 20

    DropDown2 {
        id: omegaType
        label: "Type"
        model: ["Fixed Value",
                "Turbulent Mixing Length Frequency Inlet",
                "Zero Gradient"]
        path: "boundary:omega_boundary_condition_type"
    }

    ValueField {
        enabled: (["Fixed Value"]).indexOf(omegaType.currentText) >= 0
        label: "Value [1/s]"
        path: "boundary:omega_field_value"
    }

    ValueField {
        enabled: (["Turbulent Mixing Length Frequency Inlet"
            ]).indexOf(omegaType.currentText) >= 0
        label: "Mixing Length [m]"
        path: "boundary:omega_mixing_length_value"
    }
}
