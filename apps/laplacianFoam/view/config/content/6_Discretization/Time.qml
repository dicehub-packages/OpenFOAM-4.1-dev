import QtQuick 2.5

import DICE.App 1.0
import DICE.Components 1.0

Column {
    width: parent.width

    spacing: 5

    ValueConnector {
        id: timeScheme
        path: "foam:system/fvSchemes ddtSchemes default"
    }

    ValueConnector {
        id: timeSchemeTuple
        path: "foam:system/fvSchemes ddtSchemes default %tuple"
    }

    RadioButton {
        text: "Steady State"
        checked: timeScheme.value === "steadyState"
        onClicked: timeScheme.value = "steadyState"
    }

    RadioButton {
        text: "Implicit Euler"
        checked: timeScheme.value === "Euler"
        onClicked: timeScheme.value = "Euler"
    }

    RadioButton {
        id: crankNicolson
        text: "Crank Nicolson"
        checked: !!timeSchemeTuple.value && timeScheme.value[0] === "CrankNicolson"
        onClicked: {
            timeSchemeTuple.value = ["CrankNicolson", 0.5];
        }
    }

    ValueField {
        label: ""
        visible: crankNicolson.checked
        path: visible ? "foam:system/fvSchemes ddtSchemes default 1" : ""
    }

    RadioButton {
        text: "Backward"
        checked: timeScheme.value === "backward"
        onClicked: timeScheme.value = "backward"
    }

    RadioButton {
        text: "Local Euler"
        checked: timeScheme.value === "localEuler"
        onClicked: timeScheme.value = "localEuler"
    }
}
