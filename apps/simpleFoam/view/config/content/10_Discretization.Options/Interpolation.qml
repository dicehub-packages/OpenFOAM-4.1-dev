import QtQuick 2.9

import DICE.App 1.0


Column {
    width: parent.width

    spacing: 5

    DiceValueConnector {
        id: interpolationScheme
        path: "foam:system/fvSchemes interpolationSchemes default"
    }

    DiceRadioButton {
        text: "Linear"
        checked: interpolationScheme.value === "linear"
        onClicked: interpolationScheme.value = "linear"
    }

    DiceRadioButton {
        text: "Cubic"
        checked: interpolationScheme.value === "cubic"
        onClicked: interpolationScheme.value = "cubic"
    }
}
