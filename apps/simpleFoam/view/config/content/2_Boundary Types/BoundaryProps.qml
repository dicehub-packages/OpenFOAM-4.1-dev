import QtQuick 2.5

import DICE.App 1.0
import DICE.Components 1.0

Column {
    spacing: 10
    width: parent.width
    height: childrenRect.height

    ValueConnector {
        id: isCyclic
        path: 'boundary:is_cyclic'
    }

    ValueConnector {
        id: neighbourPatch
        path: 'boundary:neighbour_patch'
    }

    DropDown2 {
        id: typeDropDown
        label: qsTr('Type')
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
        BasicText {
            width: parent.width/2
            text: "Neighbour Patch:"
        }
        BasicText {
            width: parent.width/2
            text: !!neighbourPatch.value ? neighbourPatch.value : ""
        }
    }

    DropDown2 {
        enabled: !!isCyclic.value
        visible: enabled
        label: "Transform"
        model: ["noOrdering", "translational", "rotational"]
        path: "boundary:transform"
    }

    ValueField {
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

    ValueField {
        enabled: !!isCyclic.value && !!lowLevelCorrectionEnable.value
        visible: enabled
        label: "Low Weight Correction"
        path: "boundary:low_weight_correction"
    }
}