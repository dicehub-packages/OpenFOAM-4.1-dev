import QtQuick 2.9

import DICE.App 1.0


Column {
    id: root

    property var path
    property var grad

    width: parent.width
    spacing: 5

    DiceValueConnector {
        id: gradScheme
        path: root.path + " " + root.grad
    }

    DiceValueConnector {
        id: gradSchemeTuple
        path: gradScheme.path + " %tuple"
    }

    Subheader {
        text: "Gradient"
    }

    DiceRadioButton {
        id: useDefault

        text: "Use Default Values"
        checked: gradScheme.value === undefined
        onClicked: {
            gradScheme.value = undefined
        }
        visible: root.grad !== "default"
    }

    DiceRadioButton {
        id: gauss
        text: "Gauss"
        checked: !!gradSchemeTuple.value && gradSchemeTuple.value[0] === "Gauss"
        onClicked: {
            gradSchemeTuple.value =  ["Gauss", "linear"];
        }
    }
    DiceInlineComboBox {
        visible: gauss.checked
        path: visible ? gradScheme.path + " 1" : ""
        model: ["linear", "cubic"]
    }
    DiceRadioButton {
        text: "Least Squares"
        checked: gradScheme.value === "leastSquares"
        onClicked: gradScheme.value = "leastSquares"
    }
    DiceRadioButton {
        text: "Point Linear"
        checked: gradScheme.value === "pointLinear"
        onClicked: gradScheme.value = "pointLinear"
    }
    DiceRadioButton {
        text: "Fourth"
        checked: gradScheme.value === "fourth"
        onClicked: gradScheme.value = "fourth"
    }
    DiceRadioButton {
        text: "Point Cells Least Squares"
        checked: gradScheme.value === "pointCellsLeastSquares"
        onClicked: gradScheme.value = "pointCellsLeastSquares"
    }
    DiceRadioButton {
        text: "Edge Cells Least Squares"
        checked: gradScheme.value === "edgeCellsLeastSquares"
        onClicked: gradScheme.value = "edgeCellsLeastSquares"
    }
}
