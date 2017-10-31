import QtQuick 2.9

import DICE.Components 1.0 as DC
import DICE.App 1.0

Column {
    width: parent.width
    height: childrenRect.height
    spacing: 20
    
    Row {
        width: parent.width
        spacing: 10

        DiceRadioButton {
            id: spanXYradioButton
            text: "XY"
            checked: true
        }
        DiceRadioButton {
            id: spanXZradioButton
            text: "XZ"
        }
        DiceRadioButton {
            id: spanYZradioButton
            text: "YZ"
        }
    }

    Subheader {
        text: "Origin"
    }
    DiceVectorField {
        path: "refinement:SearchablePlate.origin"
    }

    Subheader {
        text: "Span"
    }
    DC.HighlightBasicText {
        text: "One dimension needs to be 0"
        type: "info"
    }
    DiceVectorField {
        path: "refinement:SearchablePlate.span"
        xLabel: "Δx"
        yLabel: "Δy"
        zLabel: "Δz"
        xEnabled: spanXYradioButton.checked || spanXZradioButton.checked
        yEnabled: spanXYradioButton.checked || spanYZradioButton.checked
        zEnabled: spanXZradioButton.checked || spanYZradioButton.checked
        onXEnabledChanged: {
            value0 = 0
        }
        onYEnabledChanged: {
            value1 = 0
        }
        onZEnabledChanged: {
            value2 = 0
        }
    }

}
