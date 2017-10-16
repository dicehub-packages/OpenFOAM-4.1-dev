import QtQuick.Controls 1.4
import QtQuick 2.5
import QtQml.Models 2.2
import QtQuick.Layouts 1.3

import DICE.App 1.0
import DICE.Components 1.0

SolverControl {
    path: {
        switch (modelData.modelData) {
            case 'p - Pressure':
                return "foam:system/fvSolution solvers p"
            case 'U - Velocity':
                return "foam:system/fvSolution solvers U"
            case 'k':
                return "foam:system/fvSolution solvers k"
            case 'Epsilon':
                return "foam:system/fvSolution solvers epsilon"
            case 'Omega':
                return "foam:system/fvSolution solvers omega"
        }
    }
    model: [
      "PCG",
      "GAMG",
      "smoothSolver",
      "ICCG"
    ]
}

