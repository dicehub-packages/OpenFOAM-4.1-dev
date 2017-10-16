import DICE.App 1.0
import DICE.App.Foam 1.0

Body {
    Card {
        spacing: 30
        
        title: qsTr('Snapping')

        ToggleButton {
            label: "Activate Snapping"
            uncheckedText: "No"
            checkedText: "Yes"
            path: "foam:system/snappyHexMeshDict snap"
        }

        Subheader { text: "Settings for the Snapping" }

        ToggleButton {
            label: "Implicit Feature Snap"
            uncheckedText: "Off"
            checkedText: "On"
            path: "foam:system/snappyHexMeshDict snapControls implicitFeatureSnap"
        }
        ToggleButton {
            label: "Explicit Feature Snap"
            uncheckedText: "Off"
            checkedText: "On"
            path: "foam:system/snappyHexMeshDict snapControls explicitFeatureSnap"
        }
        ToggleButton {
            label: "Multi Region Feature Snap"
            uncheckedText: "Off"
            checkedText: "On"
            path: "foam:system/snappyHexMeshDict snapControls multiRegionFeatureSnap"
        }
        ValueField {
            label: "nSmoothPatch"
            path: "foam:system/snappyHexMeshDict snapControls nSmoothPatch"
            dataType: "int"
        }
        ValueField {
            label: "tolerance"
            path: "foam:system/snappyHexMeshDict snapControls tolerance"
        }
        ValueField {
            label: "nSolveIter"
            path: "foam:system/snappyHexMeshDict snapControls nSolveIter"
            dataType: "int"
        }
        ValueField {
            label: "nRelaxIter"
            path: "foam:system/snappyHexMeshDict snapControls nRelaxIter"
            dataType: "int"
        }
        ValueField {
            label: "nFeatureSnapIter"
            path: "foam:system/snappyHexMeshDict snapControls nFeatureSnapIter"
            dataType: "int"
        }
    }
}
