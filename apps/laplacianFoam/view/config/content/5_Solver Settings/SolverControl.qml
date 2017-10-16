import DICE.App 1.0
import DICE.App.Foam 1.0

Card {
    id: root

    property string path
    property alias model: linearMatrixSolver.model
    spacing: 20

    DropDown2 {
        id: linearMatrixSolver
        path: root.path + " solver"
        label: qsTr("Solver")
    }

    Subheader { text: qsTr("Options") }

    PCGoptions {}
    GAMGoptions {}
    SmoothSolverOptions {}
    ICCGoptions {}
}
