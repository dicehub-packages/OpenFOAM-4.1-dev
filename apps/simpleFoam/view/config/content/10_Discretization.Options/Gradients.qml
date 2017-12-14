import QtQuick 2.9
import QtQuick.Controls 2.2 as QQC

import DICE.App 1.0

Column {
    spacing: 10
    width: parent.width

    TabsCard3 {
        model: {
            switch (app.turbulence.model) {
            case 'laminar':
                return [
                        'Default',
                        'Velocity',
                        'Pressure'
                        ]
            case 'kOmegaSST':
                return [
                        'Default',
                        'Velocity',
                        'Pressure',
                        'k',
                        'Omega'
                        ]
            case 'kEpsilon': [
                        'Default',
                        'Velocity',
                        'Pressure',
                        'k',
                        'Epsilon'
                ]
            }
        }
        delegateSource: "GradientsLoader.qml"
        textRole: 'modelData'
    }

    Card {
        title: "Surface Normal Gradient"
        width: parent.width

        DiceValueConnector {
            id: snGradScheme
            path: "foam:system/fvSchemes snGradSchemes default"

            QQC.ButtonGroup { id: snGradientGroup }
        }

        DiceValueConnector {
            id: snGradSchemeTuple
            path: "foam:system/fvSchemes snGradSchemes default %tuple"
        }


        DiceRadioButton {
            text: "Corrected"
            checked: snGradScheme.value === "corrected"
            onClicked: snGradScheme.value = "corrected"
            QQC.ButtonGroup.group: snGradientGroup
        }

        DiceRadioButton {
            text: "Uncorrected"
            checked: snGradScheme.value === "uncorrected"
            onClicked: snGradScheme.value = "uncorrected"
            QQC.ButtonGroup.group: snGradientGroup
        }

        DiceRadioButton {
            id: limited
            text: "Limited"
            checked: !!snGradSchemeTuple.value && snGradSchemeTuple.value[0] === "limited"
            onClicked: {
                snGradSchemeTuple.value = ["limited", "corrected", 0.5];
            }
            QQC.ButtonGroup.group: snGradientGroup
        }

        DiceValueField {
            visible: limited.checked
            label: "Limiter Value"
            path: visible ? "foam:system/fvSchemes snGradSchemes default 2" : ""
        }

        DiceRadioButton {
            text: "Orthogonal"
            checked: snGradScheme.value === "orthogonal"
            onClicked: snGradScheme.value = "orthogonal"
            QQC.ButtonGroup.group: snGradientGroup
        }
    }
}
