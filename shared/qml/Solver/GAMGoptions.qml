import QtQuick 2.7
import DICE.App 1.0
import DICE.App.Foam 1.0

Column {
    width: parent.width
    spacing: 20

    enabled: linearMatrixSolver.currentText === "GAMG"
    visible: enabled

    onEnabledChanged: {
        if (enabled) {
            if (agglomerator.target.value === undefined)
                agglomerator.target.value = "faceAreaPair";
            if (mergeLevels.target.value === undefined)
                mergeLevels.target.value = 1;
        } else {
            agglomerator.target.value = undefined;
            mergeLevels.target.value = undefined;
        }
    }

    DiceInlineComboBox {
        id: agglomerator
        label: qsTr("Agglomerator")
        model: ["faceAreaPair"]
        path: root.path + " agglomerator"
    }

    DiceValueField {
        id: mergeLevels
        label: qsTr("Merge Levels")
        path: root.path + " mergeLevels"
        dataType: "int"
    }

    DiceInlineComboBox {
        id: gamgPreconditioner
        label: qsTr("Preconditioner")
        model: [
            "diagonal",
            "DIC",
            "FDIC",
            "GAMG",
            "none"
        ]
        path: root.path + " preconditioner"
        function valueFromText(txt) {
            if (txt === 'GAMG') {
                return {
                    "agglomerator": "faceAreaPair",
                    "cacheAgglomeration": true,
                    "mergeLevels": 1,
                    "preconditioner": "DIC",
                    "nCellsInCoarsestLevel": 200,
                    "tolerance": 1e-06,
                    "relTol": 0,
                    "minIter": 0,
                    "maxIter": 1000,
                    "smoother": "GaussSeidel",
                    "nPreSweeps": 0,
                    "preSweepsLevelMultiplier": 1,
                    "nPostSweeps": 2,
                    "postSweepsLevelMultiplier": 1,
                    "maxPostSweeps": 4,
                    "nFinestSweeps": 2,
                    "interpolateCorrection": false,
                    "directSolveCoarsest": false
                };
            }
            if (txt === 'none') {
                return false
            }
            return txt;
        }
        function textFromValue(val) {
            if (typeof val === 'object') {
                return 'GAMG';
            }
            if (val === false) {
                return 'none'
            }
            return val;
        }
    }

    GAMGpreconditionerOptions {
        id: gamgOptions
        enabled: gamgPreconditioner.currentText === "GAMG"
        visible: enabled
        path: root.path + " preconditioner"
    }

    DiceValueField {
        label: qsTr("Tolerance")
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
}
