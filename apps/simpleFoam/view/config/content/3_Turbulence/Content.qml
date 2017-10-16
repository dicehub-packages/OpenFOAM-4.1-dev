import QtQuick 2.4
import QtQuick.Layouts 1.3
import QtQuick.Controls 1.4

import DICE.App 1.0

Body {
    Card {
        title: qsTr("Turbulence model")

        DropDown2 {
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
            visible: app.turbulenceModel == "kOmegaSST"
            spacing: 20

            Subheader {
                text: "kOmegaSSTCoeffs"
            }

            ValueField {
                label: "alphaK1"
                path: "foam:constant/turbulenceProperties RAS kOmegaSSTCoeffs alphaK1"
            }
            ValueField {
                label: "alphaOmega2"
                path: "foam:constant/turbulenceProperties RAS kOmegaSSTCoeffs alphaOmega2"
            }
            ValueField {
                label: "gamma2"
                path: "foam:constant/turbulenceProperties RAS kOmegaSSTCoeffs gamma2"
            }
            ValueField {
                label: "alphaK2"
                path: "foam:constant/turbulenceProperties RAS kOmegaSSTCoeffs alphaK2"
            }
            ValueField {
                label: "alphaOmega1"
                path: "foam:constant/turbulenceProperties RAS kOmegaSSTCoeffs alphaOmega1"
            }
            ValueField {
                label: "gamma1"
                path: "foam:constant/turbulenceProperties RAS kOmegaSSTCoeffs gamma1"
            }
            ToggleButton {
                label: "F3"
                path: "foam:constant/turbulenceProperties RAS kOmegaSSTCoeffs F3"
            }
            ValueField {
                label: "c1"
                path: "foam:constant/turbulenceProperties RAS kOmegaSSTCoeffs c1"
            }
            ValueField {
                label: "b1"
                path: "foam:constant/turbulenceProperties RAS kOmegaSSTCoeffs b1"
            }
            ValueField {
                label: "a1"
                path: "foam:constant/turbulenceProperties RAS kOmegaSSTCoeffs a1"
            }
            ValueField {
                label: "beta1"
                path: "foam:constant/turbulenceProperties RAS kOmegaSSTCoeffs beta1"
            }
            ValueField {
                label: "beta2"
                path: "foam:constant/turbulenceProperties RAS kOmegaSSTCoeffs beta2"
            }
            ValueField {
                label: "betaStar"
                path: "foam:constant/turbulenceProperties RAS kOmegaSSTCoeffs betaStar"
            }
        }

    }




}
