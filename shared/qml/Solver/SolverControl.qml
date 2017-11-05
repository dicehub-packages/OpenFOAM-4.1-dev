import QtQuick 2.7

import DICE.App 1.0
import DICE.App.Foam 1.0

Column {
    id: root

    property string path
    property alias model: linearMatrixSolver.model
    spacing: 20

    DiceInlineComboBox {
        id: linearMatrixSolver
        path: root.path + " solver"
        label: qsTr("Solver")
    }

    Subheader {
        text: qsTr("Options")
        horizontalAlignment: "AlignHCenter"
    }

    PCGoptions {}
    GAMGoptions {}
    SmoothSolverOptions {}
    ICCGoptions {}
}
