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
    model: {
        switch (modelData.modelData) {
           case 'Pressure':
               return ["PCG", "GAMG", "smoothSolver", "ICCG"]
           case 'Velocity':
               return ["PCG", "smoothSolver", "ICCG"]
           case 'k':
               return ["PCG", "smoothSolver", "ICCG"]
           case 'Epsilon':
               return ["PCG", "smoothSolver", "ICCG"]
           case 'Omega':
               return ["PCG", "smoothSolver", "ICCG"]
       }
    }
}

