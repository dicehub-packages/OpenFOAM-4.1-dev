import QtQuick.Controls 1.4
import QtQuick 2.5

import DICE.App 1.0

Body {
    Card {
        title: qsTr("Castellating")
        spacing: 30

        DiceSwitch {
            text: "Enable CastellatedMesh"
            path: "foam:system/snappyHexMeshDict castellatedMesh"
        }
        DiceValueField {
            label: qsTr("Resolve Feature Angle [°]")
            path: "foam:system/snappyHexMeshDict castellatedMeshControls resolveFeatureAngle"
            dataType: "int"
        }
        Row {
            width: parent.width
            DiceCheckBox{
                id: gapLevelIncrementOption
                checked: typeof gapLevelIncrement.value !== 'undefined'
                onClicked: gapLevelIncrement.setValue(checked? 0: undefined)
            }
            DiceValueField {
                id: gapLevelIncrement
                enabled: gapLevelIncrementOption.checked
                label: qsTr("Gap Level Increment")
                path: "foam:system/snappyHexMeshDict castellatedMeshControls gapLevelIncrement"
                dataType: "int"
                width: parent.width - gapLevelIncrementOption.width
            }
        }
        Row {
            width: parent.width

            DiceCheckBox {
                id: planarAngleOption
                checked: typeof planarAngle.value !== 'undefined'
                onClicked: planarAngle.setValue(checked? 0: undefined)
            }
            DiceValueField {
                id: planarAngle
                enabled: planarAngleOption.checked
                label: qsTr("Planar Angle [°]")
                path: "foam:system/snappyHexMeshDict castellatedMeshControls planarAngle"
                dataType: "int"
                width: parent.width - planarAngleOption.width
            }
        }
        DiceValueField {
            label: qsTr("Maximum Local Cells")
            path: "foam:system/snappyHexMeshDict castellatedMeshControls maxLocalCells"
            dataType: "int"
        }
        DiceValueField {
            label: qsTr("Maximum Global Cells")
            path: "foam:system/snappyHexMeshDict castellatedMeshControls maxGlobalCells"
            dataType: "int"
        }
        DiceValueField {
            label: qsTr("Minimum Refinement Cells")
            path: "foam:system/snappyHexMeshDict castellatedMeshControls minRefinementCells"
            dataType: "int"
        }
        DiceValueField {
            label: qsTr("Number of Cells between Levels")
            path: "foam:system/snappyHexMeshDict castellatedMeshControls nCellsBetweenLevels"
            dataType: "int"
        }
        DiceSwitch {
            text: qsTr("Allow Free Standing Zone Faces")
            path: "foam:system/snappyHexMeshDict castellatedMeshControls allowFreeStandingZoneFaces"
        }
    }
}
