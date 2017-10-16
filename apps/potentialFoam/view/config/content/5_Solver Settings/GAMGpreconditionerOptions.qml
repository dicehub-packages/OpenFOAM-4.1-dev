import QtQuick 2.7
import DICE.App 1.0
import DICE.App.Foam 1.0

Column {
    id: root
    
    property string path

    height: childrenRect.height
    width: parent.width
    spacing: 20

    Subheader { text: qsTr("GAMG Preconditioner Options") }

    DropDown2 {
        label: qsTr("Agglomerator")
        model: ["faceAreaPair"]
        path: root.path + " agglomerator"
    }

    ToggleButton2 {
        label: qsTr("Cache Agglomeration")
        path: root.path + " cacheAgglomeration"
    }

    ValueField {
        label: qsTr("Merge Levels")
        path: root.path + " mergeLevels"
        dataType: "int"
    }

    ValueField {
        label: qsTr("Tolerance")
        path: root.path + " nCellsInCoarsestLevel"
    }

    ValueField {
        label: qsTr("Relative Tolerance")
        path: root.path + " tolerance"
    }

    ValueField {
        label: qsTr("Relative Tolerance")
        path: root.path + " relTol"
    }

    ValueField {
        label: qsTr("Minimum Iterations")
        path: root.path + " minIter"
        dataType: "int"
    }

    ValueField {
        label: qsTr("Maximum Iterations")
        path: root.path + " maxIter"
        dataType: "int"
    }

    DropDown2 {
        label: qsTr("Smoother")
        model: [
            "DIC",
            "DICGaussSeidel",
            "FDIC",
            "GaussSeidel",
            "nonBlockingGaussSeidel",
            "symGaussSeidel"
        ]
        path: root.path + " smoother"
    }

    ValueField {
        label: qsTr("Pre Sweeps")
        path: root.path + " nPreSweeps"
        dataType: "int"
    }

    ValueField {
        label: qsTr("Pre Sweeps Level Multiplier")
        path: root.path + " preSweepsLevelMultiplier"
        dataType: "int"
    }

    ValueField {
        label: qsTr("Post Sweeps")
        path: root.path + " nPostSweeps"
        dataType: "int"
    }

    ValueField {
        label: qsTr("Post Sweeps Level Multiplier")
        path: root.path + " postSweepsLevelMultiplier"
        dataType: "int"
    }

    ValueField {
        label: qsTr("Max Post Sweeps")
        path: root.path + " maxPostSweeps"
        dataType: "int"
    }

    ValueField {
        label: qsTr("Finest Sweeps")
        path: root.path + " nFinestSweeps"
        dataType: "int"
    }

    ToggleButton2 {
        label: qsTr("Interpolate Correction")
        path: root.path + " interpolateCorrection"
    }

    ToggleButton2 {
        label: qsTr("Direct Solve Coarsest")
        path: root.path + " directSolveCoarsest"
    }
}
