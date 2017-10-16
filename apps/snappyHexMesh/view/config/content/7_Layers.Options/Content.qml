import DICE.App 1.0
import DICE.App.Foam 1.0

Body {
    Card {
        title: qsTr('Layers')
        spacing: 30
        ToggleButton {
            label: "Add Layers"
            uncheckedText: "No"
            checkedText: "Yes"
            path: "foam:system/snappyHexMeshDict addLayers"
        }
        Subheader { text: "Settings for Layer Addition" }
        ToggleButton {
            id: toggleButtonRelativeSize
            uncheckedText:  "Absolute Sizes [m]"
            checkedText: "Relative Sizes [-]"
            path: "foam:system/snappyHexMeshDict addLayersControls relativeSizes"
        }
        ValueField {
            label: "Expansion Ratio"
            path: "foam:system/snappyHexMeshDict addLayersControls expansionRatio"
        }
        ValueField {
            label: "Final Layer Thickness"
            path: "foam:system/snappyHexMeshDict addLayersControls finalLayerThickness"
        }
        ValueField {
            label: "Minimum Thickness"
            path: "foam:system/snappyHexMeshDict addLayersControls minThickness"
        }
        ValueField {
            label: "nGrow"
            path: "foam:system/snappyHexMeshDict addLayersControls nGrow"
            dataType: "int"
        }
    }
    Card {
        spacing: 30
        title: qsTr('Advanced Settings')

        ValueField {
            label: "Feature Angle [°]"
            path: "foam:system/snappyHexMeshDict addLayersControls featureAngle"
            dataType: "int"
        }
        ValueField {
            label: "nRelaxIter"
            path: "foam:system/snappyHexMeshDict addLayersControls nRelaxIter"
            dataType: "int"
        }
        ValueField {
            label: "nSmoothSurfaceNormals"
            path: "foam:system/snappyHexMeshDict addLayersControls nSmoothSurfaceNormals"
            dataType: "int"
        }
        ValueField {
            label: "nSmoothNormals"
            path: "foam:system/snappyHexMeshDict addLayersControls nSmoothNormals"
            dataType: "int"
        }
        ValueField {
            label: "nSmoothThickness"
            path: "foam:system/snappyHexMeshDict addLayersControls nSmoothThickness"
            dataType: "int"
        }
        ValueField {
            label: "maxFaceThicknessRatio"
            path: "foam:system/snappyHexMeshDict addLayersControls maxFaceThicknessRatio"
        }
        ValueField {
            label: "maxThicknessToMedialRatio"
            path: "foam:system/snappyHexMeshDict addLayersControls maxThicknessToMedialRatio"
        }
        ValueField {
            label: "minMedianAxisAngle [°]"
            path: "foam:system/snappyHexMeshDict addLayersControls minMedianAxisAngle"
            dataType: "int"
        }
        ValueField {
            label: "nBufferCellsNoExtrude"
            path: "foam:system/snappyHexMeshDict addLayersControls nBufferCellsNoExtrude"
            dataType: "int"
        }
        ValueField {
            label: "nLayerIter"
            path: "foam:system/snappyHexMeshDict addLayersControls nLayerIter"
            dataType: "int"
        }
    }
}
