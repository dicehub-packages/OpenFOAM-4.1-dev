import QtQuick 2.9

import DICE.App 1.0


Body {
    Card {
        title: qsTr("Turbulence model")

        DiceComboBox {
            target: app
            property: "turbulenceModel"
            model: [
                "laminar",
                "kOmegaSST",
                "kEpsilon"
            ]
        }

        Card {
            title: "kEpsilonCoeffs"
            width: parent.width
            visible: app.turbulenceModel === "kEpsilon"
            spacing: 20
            expanded: false
            backgroundBorder: 0

            DiceValueField {
                label: "Cmu"
                path: "foam:constant/turbulenceProperties RAS kEpsilonCoeffs Cmu"
            }
            DiceValueField {
                label: "C1"
                path: "foam:constant/turbulenceProperties RAS kEpsilonCoeffs C1"
            }
            DiceValueField {
                label: "C2"
                path: "foam:constant/turbulenceProperties RAS kEpsilonCoeffs C2"
            }
            DiceValueField {
                label: "C3"
                path: "foam:constant/turbulenceProperties RAS kEpsilonCoeffs C3"
            }
            DiceValueField {
                label: "sigmak"
                path: "foam:constant/turbulenceProperties RAS kEpsilonCoeffs sigmak"
            }
            DiceValueField {
                label: "sigmaEps"
                path: "foam:constant/turbulenceProperties RAS kEpsilonCoeffs sigmaEps"
            }
        }

        Card {
            title: "kOmegaSSTCoeffs"
            width: parent.width
            visible: app.turbulenceModel === "kOmegaSST"
            spacing: 20
            expanded: false
            backgroundBorder: 0

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
            DiceSwitch {
                text: "F3"
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
