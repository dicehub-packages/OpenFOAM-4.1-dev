SolverControl {
    path: {
        switch (modelData.modelData) {
            case 'Pressure':
                return "foam:system/fvSolution solvers p"
            case 'Velocity':
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

