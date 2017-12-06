import QtQuick 2.9

import DICE.App 1.0


Column {
    id: root

    spacing: 10
    height: childrenRect.height
    width: parent.width

    DiceSwitch {
        id: enabledSurfaceRefinement
        text: "Enable surface refinement"
        path: "refinement:RefinementObject.refinement_surface_is_enabled"
    }

    DiceVectorField2D2 {
        xLabel: "Min Level"
        yLabel: "Max Level"
        dataType: "int"
        path: "refinement:RefinementObject.surface_level"
        enabled: enabledSurfaceRefinement.checked
        visible: enabled
    }

    DiceSwitch {
        id: convertToRegion
        text: qsTr("Convert to Region")
        path: "refinement:RefinementObject.is_region"
        enabled: enabledSurfaceRefinement.checked
        visible: enabled
    }

    Column {
        spacing: 10
        enabled: convertToRegion.checked
                 && enabledSurfaceRefinement.checked
        visible: enabled
        height: enabled ? childrenRect.height : 0
        width: parent.width

        Subheader {
            text: "Cell Zone Type"
        }
        DiceComboBox {
            model: ["inside", "outside"]
            path: "refinement:RefinementObject.cell_zone_inside"
        }

        Subheader {
            text: "Face Zone Type"
        }
        DiceComboBox {
            model: ["internal", "baffle", "boundary"]
            path: "refinement:RefinementObject.face_type"
        }
    }
}
