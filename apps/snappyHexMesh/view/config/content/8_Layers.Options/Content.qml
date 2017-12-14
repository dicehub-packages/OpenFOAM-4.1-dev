import DICE.App 1.0

Body {
    Card {
        title: qsTr('Layers')
        spacing: 30
        DiceSwitch {
            text: "Add Layers"
            path: "foam:system/snappyHexMeshDict addLayers"
        }
        ToggleButton {
            id: toggleButtonRelativeSize
            uncheckedText:  "Absolute Sizes [m]"
            checkedText: "Relative Sizes [-]"
            path: "foam:system/snappyHexMeshDict addLayersControls relativeSizes"
        }
        DiceValueField {
            label: "Expansion Ratio"
            path: "foam:system/snappyHexMeshDict addLayersControls expansionRatio"
        }
        DiceValueField {
            label: "Final Layer Thickness"
            path: "foam:system/snappyHexMeshDict addLayersControls finalLayerThickness"
        }
        DiceValueField {
            label: "Minimum Thickness"
            path: "foam:system/snappyHexMeshDict addLayersControls minThickness"
        }
        DiceValueField {
            label: "nGrow"
            path: "foam:system/snappyHexMeshDict addLayersControls nGrow"
            dataType: "int"
        }
    }
    Card {
        spacing: 30
        title: qsTr('Advanced Settings')

        DiceValueField {
            label: "Feature Angle [°]"
            path: "foam:system/snappyHexMeshDict addLayersControls featureAngle"
            dataType: "int"
        }
        DiceValueField {
            label: "nRelaxIter"
            path: "foam:system/snappyHexMeshDict addLayersControls nRelaxIter"
            dataType: "int"
        }
        DiceValueField {
            label: "nSmoothSurfaceNormals"
            path: "foam:system/snappyHexMeshDict addLayersControls nSmoothSurfaceNormals"
            dataType: "int"
        }
        DiceValueField {
            label: "nSmoothNormals"
            path: "foam:system/snappyHexMeshDict addLayersControls nSmoothNormals"
            dataType: "int"
        }
        DiceValueField {
            label: "nSmoothThickness"
            path: "foam:system/snappyHexMeshDict addLayersControls nSmoothThickness"
            dataType: "int"
        }
        DiceValueField {
            label: "maxFaceThicknessRatio"
            path: "foam:system/snappyHexMeshDict addLayersControls maxFaceThicknessRatio"
        }
        DiceValueField {
            label: "maxThicknessToMedialRatio"
            path: "foam:system/snappyHexMeshDict addLayersControls maxThicknessToMedialRatio"
        }
        DiceValueField {
            label: "minMedianAxisAngle [°]"
            path: "foam:system/snappyHexMeshDict addLayersControls minMedianAxisAngle"
            dataType: "int"
        }
        DiceValueField {
            label: "nBufferCellsNoExtrude"
            path: "foam:system/snappyHexMeshDict addLayersControls nBufferCellsNoExtrude"
            dataType: "int"
        }
        DiceValueField {
            label: "nLayerIter"
            path: "foam:system/snappyHexMeshDict addLayersControls nLayerIter"
            dataType: "int"
        }
    }
}
