import QtQuick 2.9

import DICE.App 1.0


Column {
    spacing: 10
    width: parent.width
    height: childrenRect.height

    Subheader {
        text: "Add Your Monitor"
        horizontalAlignment: "AlignHCenter"
    }

    DiceButton {
        text: "Add Forces Monitor"
        onClicked: app.functionObjects.addFunctionObject("forces")
    }

    DiceButton {
        text: "Add Forces Coefficients Monitor"
        onClicked: app.functionObjects.addFunctionObject("forceCoeffs")
    }
}
