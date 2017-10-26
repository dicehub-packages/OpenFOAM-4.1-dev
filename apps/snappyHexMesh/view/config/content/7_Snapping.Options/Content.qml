import DICE.App 1.0
import DICE.App.Foam 1.0

Body {
    Card {
        spacing: 30
        
        title: qsTr('Snapping')

        DiceSwitch {
            text: "Activate Snapping"
            path: "foam:system/snappyHexMeshDict snap"
        }

        Subheader {
            text: "Settings for the Snapping"
            horizontalAlignment: "AlignHCenter"
        }

        DiceSwitch {
            text: "Implicit Feature Snap"
            path: "foam:system/snappyHexMeshDict snapControls implicitFeatureSnap"
        }
        DiceSwitch {
            text: "Explicit Feature Snap"
            path: "foam:system/snappyHexMeshDict snapControls explicitFeatureSnap"
        }
        DiceSwitch {
            text: "Multi Region Feature Snap"
            path: "foam:system/snappyHexMeshDict snapControls multiRegionFeatureSnap"
        }
        DiceValueField {
            label: "nSmoothPatch"
            path: "foam:system/snappyHexMeshDict snapControls nSmoothPatch"
            dataType: "int"
        }
        DiceValueField {
            label: "tolerance"
            path: "foam:system/snappyHexMeshDict snapControls tolerance"
        }
        DiceValueField {
            label: "nSolveIter"
            path: "foam:system/snappyHexMeshDict snapControls nSolveIter"
            dataType: "int"
        }
        DiceValueField {
            label: "nRelaxIter"
            path: "foam:system/snappyHexMeshDict snapControls nRelaxIter"
            dataType: "int"
        }
        DiceValueField {
            label: "nFeatureSnapIter"
            path: "foam:system/snappyHexMeshDict snapControls nFeatureSnapIter"
            dataType: "int"
        }
    }
}
