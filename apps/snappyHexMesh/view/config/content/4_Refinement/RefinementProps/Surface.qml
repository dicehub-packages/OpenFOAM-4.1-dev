import QtQuick 2.9

import DICE.App 1.0


Column {
    id: root

    spacing: 10
    height: childrenRect.height
    width: parent.width

    DiceVectorField2D2 {
        xLabel: "Min Level"
        yLabel: "Max Level"
        dataType: "int"
        path: "refinement:Surface.surface_level"
    }

    DiceSwitch {
        id: convertToRegion
        text: qsTr("Convert to Region")
        path: "refinement:Surface.is_region"
    }

    Column {
        spacing: 10
        enabled: convertToRegion.checked
        visible: enabled
//        height: enabled ? childrenRect.height : 0
        width: parent.width

        Subheader {
            text: "Cell Zone Type"
        }
        DiceComboBox {
            model: ["inside", "outside"]
            path: "refinement:Surface.cell_zone_inside"
        }

        Subheader {
            text: "Face Zone Type"
        }
        DiceComboBox {
            model: ["internal", "baffle", "boundary"]
            path: "refinement:Surface.face_type"
        }
    }
}
