import QtQuick 2.4
import QtQuick.Layouts 1.3
import QtQuick.Controls 1.4

import DICE.App 1.0

Body {
    Card {
        title: qsTr("Turbulence model")

        DiceComboBox {
            target: app
            visible: turbToggle.checked
            property: "turbulenceModel"
            model: [
                "none",
                "kOmegaSST",
                "kEpsilon"
            ]
        }

        Column {
            width: parent.width
            visible: app.turbulenceModel === "kOmegaSST"
            spacing: 20

            Subheader {
                text: "kOmegaSSTCoeffs"
            }

            DiceValueField {
                label: "alphaK1"
                path: "foam:constant/turbulenceProperties RAS kOmegaSSTCoeffs alphaK1"
            }
            DiceValueField {
                label: "alphaOmega2"
                path: "foam:constant/turbulenceProperties RAS kOmegaSSTCoeffs alphaOmega2"
            }
            DiceValueField {
                label: "gamma2"
                path: "foam:constant/turbulenceProperties RAS kOmegaSSTCoeffs gamma2"
            }
            DiceValueField {
                label: "alphaK2"
                path: "foam:constant/turbulenceProperties RAS kOmegaSSTCoeffs alphaK2"
            }
            DiceValueField {
                label: "alphaOmega1"
                path: "foam:constant/turbulenceProperties RAS kOmegaSSTCoeffs alphaOmega1"
            }
            DiceValueField {
                label: "gamma1"
                path: "foam:constant/turbulenceProperties RAS kOmegaSSTCoeffs gamma1"
            }
            ToggleButton {
                label: "F3"
                path: "foam:constant/turbulenceProperties RAS kOmegaSSTCoeffs F3"
            }
            DiceValueField {
                label: "c1"
                path: "foam:constant/turbulenceProperties RAS kOmegaSSTCoeffs c1"
            }
            DiceValueField {
                label: "b1"
                path: "foam:constant/turbulenceProperties RAS kOmegaSSTCoeffs b1"
            }
            DiceValueField {
                label: "a1"
                path: "foam:constant/turbulenceProperties RAS kOmegaSSTCoeffs a1"
            }
            DiceValueField {
                label: "beta1"
                path: "foam:constant/turbulenceProperties RAS kOmegaSSTCoeffs beta1"
            }
            DiceValueField {
                label: "beta2"
                path: "foam:constant/turbulenceProperties RAS kOmegaSSTCoeffs beta2"
            }
            DiceValueField {
                label: "betaStar"
                path: "foam:constant/turbulenceProperties RAS kOmegaSSTCoeffs betaStar"
            }
        }

    }




}
