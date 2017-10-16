import DICE.App 1.0
import DICE.App.Foam 1.0

Body {
    SolverControl {
        title: qsTr("p - Pressure")
        path: "foam:system/fvSolution solvers p"
        model: [
	      "PCG",
	      "GAMG",
	      "smoothSolver",
	      "ICCG"
	    ]
    }
}
