import QtQuick 2.5

import DICE.App 1.0
import DICE.Components 1.0

Column {
    width: parent.width
    height: childrenRect.height

    spacing: 20

    DropDown2 {
        id: pressureType
        label: "Type"
        path: "boundary:temperature_boundary_condition_type"
        modelPath: "boundary:temperature_boundary_condition_type_list"
    }

    ValueField {
        enabled: (["Fixed Value"]).indexOf(pressureType.currentText) >= 0
        label: qsTr("Temperature [K]")
        path: "boundary:temperature_field_value"
    }
}
