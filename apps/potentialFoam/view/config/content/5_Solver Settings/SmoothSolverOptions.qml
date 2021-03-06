import QtQuick 2.7
import DICE.App 1.0
import DICE.App.Foam 1.0

Column {
    height: childrenRect.height
    width: parent.width

    spacing: 20

    enabled: linearMatrixSolver.currentText === "smoothSolver"
    visible: enabled

    onEnabledChanged: {
        if (enabled) {
            if (smoother.target.value === undefined)
                smoother.target.value = "DIC";
        } else {
            smoother.target.value = undefined;
        }
    }

    DropDown2 {
        id: smoothSolverPreconditioner
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
            if (txt == 'GAMG') {
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
            return txt;
        }
        function textFromValue(val) {
            if (typeof val === 'object') {
                return 'GAMG';
            }
            return val;
        }
    }

    GAMGpreconditionerOptions {
        enabled: smoothSolverPreconditioner.currentText === "GAMG"
        visible: enabled
        path: root.path + " preconditioner"
    }

    DropDown2 {
        id: smoother
        label: qsTr("Smoother")
        model: ["DIC",
                "DICGaussSeidel",
                "FDIC",
                "GaussSeidel",
                "nonBlockingGaussSeidel",
                "symGaussSeidel"]
        path: root.path + " smoother"
    }

    ValueField {
        label: qsTr("Tolerance")
        path: root.path + " tolerance"
    }

    ValueField {
        label: qsTr("Relative Tolerance")
        path: root.path + " relTol"
    }

    ValueField {
        label: qsTr("Minimum Iterations")
        path: root.path + " minIter"
    }

    ValueField {
        label: qsTr("Maximum Iterations")
        path: root.path + " maxIter"
    }
}
