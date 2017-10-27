import QtQuick 2.5

import DICE.App 1.0
import DICE.Components 1.0

Column {
    width: parent.width

    spacing: 5

    DiceValueConnector {
        id: interpolationScheme
        path: "foam:system/fvSchemes interpolationSchemes default"
    }

    RadioButton {
        text: "Linear"
        checked: interpolationScheme.value == "linear"
        onClicked: interpolationScheme.value = "linear"
    }

    RadioButton {
        text: "Cubic"
        checked: interpolationScheme.value == "cubic"
        onClicked: interpolationScheme.value = "cubic"
    }
}
