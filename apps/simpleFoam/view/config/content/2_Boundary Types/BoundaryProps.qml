import QtQuick 2.9

import DICE.App 1.0
import DICE.Components 1.0 as DC

Column {
    spacing: 10
    width: parent.width
    height: childrenRect.height

    DiceValueConnector {
        id: isCyclic
        path: 'boundary:is_cyclic'
    }

    DiceValueConnector {
        id: neighbourPatch
        path: 'boundary:neighbour_patch'
    }

    Subheader {
        text: "Type"
    }
    DiceComboBox {
        id: typeDropDown
        enabled: !isCyclic.value
        visible: enabled
        model: [
            "patch",
            "wall",
            "symmetryPlane",
            "symmetry",
            "empty",
            "wedge",
            "processor"
        ] 
        path: "boundary:boundary_type"
    }

    DiceButton {
        width: parent.width
        text: 'Group'
        enabled: app.canGroup
        onClicked: app.makeGroup()
    }

    Row {
        width: parent.width
        visible: !!neighbourPatch.value 
        DC.BasicText {
            width: parent.width/2
            text: "Neighbour Patch:"
        }
        DC.BasicText {
            width: parent.width/2
            text: !!neighbourPatch.value ? neighbourPatch.value : ""
        }
    }

    Subheader {
        text: "Transform"
    }
    DiceComboBox {
        enabled: !!isCyclic.value
        visible: enabled
        model: ["noOrdering", "translational", "rotational"]
        path: "boundary:transform"
    }

    DiceValueField {
        enabled: !!isCyclic.value
        visible: enabled
        label: "Match Tolerance"
        path: "boundary:match_tolerance"
    }

    CheckBoxButton2 {
        id: lowLevelCorrectionEnable
        enabled: !!isCyclic.value
        visible: enabled
        path: "boundary:low_weight_correction_enable"
    }

    DiceValueField {
        enabled: !!isCyclic.value && !!lowLevelCorrectionEnable.value
        visible: enabled
        label: "Low Weight Correction"
        path: "boundary:low_weight_correction"
    }
}
