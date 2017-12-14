import QtQuick 2.7

import DICE.App 1.0


Column {
    id: root
    
    property string path

    width: parent.width
    spacing: 20

    Subheader { text: qsTr("GAMG Preconditioner Options") }

    DiceInlineComboBox {
        label: qsTr("Agglomerator")
        model: ["faceAreaPair"]
        path: root.path + " agglomerator"
    }

    DiceSwitch {
        text: qsTr("Cache Agglomeration")
        path: root.path + " cacheAgglomeration"
    }

    DiceValueField {
        label: qsTr("Merge Levels")
        path: root.path + " mergeLevels"
        dataType: "int"
    }

    DiceValueField {
        label: qsTr("Tolerance")
        path: root.path + " nCellsInCoarsestLevel"
    }

    DiceValueField {
        label: qsTr("Relative Tolerance")
        path: root.path + " tolerance"
    }

    DiceValueField {
        label: qsTr("Relative Tolerance")
        path: root.path + " relTol"
    }

    DiceValueField {
        label: qsTr("Minimum Iterations")
        path: root.path + " minIter"
        dataType: "int"
    }

    DiceValueField {
        label: qsTr("Maximum Iterations")
        path: root.path + " maxIter"
        dataType: "int"
    }

    DiceInlineComboBox {
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

    DiceValueField {
        label: qsTr("Pre Sweeps")
        path: root.path + " nPreSweeps"
        dataType: "int"
    }

    DiceValueField {
        label: qsTr("Pre Sweeps Level Multiplier")
        path: root.path + " preSweepsLevelMultiplier"
        dataType: "int"
    }

    DiceValueField {
        label: qsTr("Post Sweeps")
        path: root.path + " nPostSweeps"
        dataType: "int"
    }

    DiceValueField {
        label: qsTr("Post Sweeps Level Multiplier")
        path: root.path + " postSweepsLevelMultiplier"
        dataType: "int"
    }

    DiceValueField {
        label: qsTr("Max Post Sweeps")
        path: root.path + " maxPostSweeps"
        dataType: "int"
    }

    DiceValueField {
        label: qsTr("Finest Sweeps")
        path: root.path + " nFinestSweeps"
        dataType: "int"
    }

    DiceSwitch {
        text: "Interpolate Correction"
        path: root.path + " interpolateCorrection"
    }
    DiceSwitch {
        text: "Direct Solve Coarsest"
        path: root.path + " directSolveCoarsest"
    }
}
