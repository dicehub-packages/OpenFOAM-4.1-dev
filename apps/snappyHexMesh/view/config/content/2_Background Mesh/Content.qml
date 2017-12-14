import QtQuick 2.9

import DICE.App 1.0

Body {
    Card {
        title: "Bounding Box"
        DiceVectorField {
            id: bbMin
            xLabel: "min X"
            yLabel: "min Y"
            zLabel: "min Z"
            target: app.boundingBox
            property: 'boundingBoxMin'
        }
        DiceVectorField {
            id: bbMax
            xLabel: "max X"
            yLabel: "max Y"
            zLabel: "max Z"
            target: app.boundingBox
            property: 'boundingBoxMax'
        }
        Caption {
            text: qsTr("Additional spacing [%]")
            horizontalAlignment: "AlignHCenter"
        }
        DiceVectorField {
            id: spacingInput
            xLabel: "Spacing X [%]"
            yLabel: "Spacing Y [%]"
            zLabel: "Spacing Z [%]"
            target: app.boundingBox
            property: 'additionalSpacing'           
        }
        DiceButton {
            id: calculateBoundingBoxButton
            width: parent.width
            text: qsTr("Calculate Automatically")
            onClicked: {
                app.boundingBox.calculateBoundingBox()
            }
        }
        Keys.onReturnPressed: {
            if (spacingInput.focus) {
                calculateBoundingBoxButton.clicked()
            }
        }
    }
    Card {
        title: "Cells"
        ToggleButton {
            id: toggleSizeOrNumber
            uncheckedText: "Number of Cells"
            checkedText: qsTr("Cells Size Δs [m]")
            target: app.boundingBox
            property: "sizeOrNumber"
        }
        DiceVectorField {
            readOnly: toggleSizeOrNumber.checked
            enabled: !readOnly
            xLabel: "Cells in X"
            yLabel: "Cells in Y"
            zLabel: "Cells in Z"
            dataType: "int"
            target: app.boundingBox
            property: 'cellsNum'
        }
        DiceVectorField {
            readOnly: !toggleSizeOrNumber.checked
            enabled: !readOnly
            xLabel: "Δs in X [m]"
            yLabel: "Δs in Y [m]"
            zLabel: "Δs in Z [m]"
            target: app.boundingBox
            property: 'cellsSize'
        }
    }
}
