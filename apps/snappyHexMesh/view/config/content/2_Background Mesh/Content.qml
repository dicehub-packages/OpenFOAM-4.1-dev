import QtQuick 2.6

import DICE.App 1.0

Body {
    Card {
        title: "Bounding Box"
        VectorField {
            id: bbMin
            xLabel: "min X"
            yLabel: "min Y"
            zLabel: "min Z"
            target: app.boundingBox
            property: 'boundingBoxMin'
        }
        VectorField {
            id: bbMax
            xLabel: "max X"
            yLabel: "max Y"
            zLabel: "max Z"
            target: app.boundingBox
            property: 'boundingBoxMax'
        }
        Caption {
            text: qsTr("Additional spacing [%]")
        }
        VectorField {
            id: spacingInput
            xLabel: "Spacing X [%]"
            yLabel: "Spacing Y [%]"
            zLabel: "Spacing Z [%]"
            target: app.boundingBox
            property: 'additionalSpacing'           
        }
        Button {
            width: parent.width
            text: qsTr("Calculate Automatically")
            onClicked: {
                app.boundingBox.calculateBoundingBox()
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
        VectorField {
            readOnly: toggleSizeOrNumber.checked
            enabled: !readOnly
            xLabel: "Cells in X"
            yLabel: "Cells in Y"
            zLabel: "Cells in Z"
            dataType: "int"
            target: app.boundingBox
            property: 'cellsNum'    
        }
        VectorField {
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
