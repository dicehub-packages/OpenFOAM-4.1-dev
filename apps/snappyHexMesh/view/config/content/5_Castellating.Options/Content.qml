import QtQuick.Controls 1.4
import QtQuick 2.5

import DICE.App 1.0

Body {
    Card {
        title: qsTr("Castellating")
        spacing: 30

        Switch {
            text: "Enable CastellatedMesh"
        }

        ToggleButton {
            label: qsTr("Activate CastellatedMesh Generation")
            uncheckedText: qsTr("No")
            checkedText: qsTr("Yes")
            path: "foam:system/snappyHexMeshDict castellatedMesh"
        }
        Subheader { text: qsTr("Settings for the castellatedMesh generation") }
        ValueField {
            label: qsTr("Resolve Feature Angle [°]")
            path: "foam:system/snappyHexMeshDict castellatedMeshControls resolveFeatureAngle"
            dataType: "int"
        }
        Row {
            width: parent.width
            CheckBox{
                id: gapLevelIncrementOption
                checked: typeof gapLevelIncrement.value !== 'undefined'
                onClicked: gapLevelIncrement.setValue(checked? 0: undefined)
            }
            ValueField {
                id: gapLevelIncrement
                enabled: gapLevelIncrementOption.checked
                label: qsTr("Gap Level Increment")
                path: "foam:system/snappyHexMeshDict castellatedMeshControls gapLevelIncrement"
                dataType: "int"
            }
        }
        Row {
            width: parent.width
            CheckBox{
                id: planarAngleOption
                checked: typeof planarAngle.value !== 'undefined'
                onClicked: planarAngle.setValue(checked? 0: undefined)
            }
            ValueField {
                id: planarAngle
                enabled: planarAngleOption.checked
                label: qsTr("Planar Angle [°]")
                path: "foam:system/snappyHexMeshDict castellatedMeshControls planarAngle"
                dataType: "int"
            }
        }
        ValueField {
            label: qsTr("Maximum Local Cells")
            path: "foam:system/snappyHexMeshDict castellatedMeshControls maxLocalCells"
            dataType: "int"
        }
        ValueField {
            label: qsTr("Maximum Global Cells")
            path: "foam:system/snappyHexMeshDict castellatedMeshControls maxGlobalCells"
            dataType: "int"
        }
        ValueField {
            label: qsTr("Minimum Refinement Cells")
            path: "foam:system/snappyHexMeshDict castellatedMeshControls minRefinementCells"
            dataType: "int"
        }
        ValueField {
            label: qsTr("Number of Cells between Levels")
            path: "foam:system/snappyHexMeshDict castellatedMeshControls nCellsBetweenLevels"
            dataType: "int"
        }
        ToggleButton {
            label: qsTr("Allow Free Standing Zone Faces")
            uncheckedText: "No"
            checkedText: "Yes"
            path: "foam:system/snappyHexMeshDict castellatedMeshControls allowFreeStandingZoneFaces"
        }
    }
}
