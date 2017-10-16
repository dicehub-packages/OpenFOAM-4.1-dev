import QtQuick 2.4
import QtQuick.Controls 1.3

import DICE.App 1.0
import DICE.App.Foam 1.0

Component {

    Body {
        width: 300

        Card {
            id: root

            ToggleButton {
                label: qsTr("Activate Parallel Run")
                methodName: "app_config"
                callParameter: "parallelRun"
            }

            Subheader{ text: qsTr("Decomposition Options") }

            FoamValue {
                label: qsTr("Number of Subdomains")
                path: "system/decomposeParDict numberOfSubdomains"
                dataType: "int"
            }

            FoamDropDown {
                id: methodDropDown

                label: qsTr("Method")
                modelPath: "decomposition methods"
                path: "system/decomposeParDict method"
            }

            Subheader { text: qsTr("Coeffs") }

            FoamDictCheck {
                id: coeffsN
                path: "system/decomposeParDict " + methodDropDown.currentText + "Coeffs n"
            }

            FoamVector {
                xLabel: "n_x"
                yLabel: "n_y"
                zLabel: "n_z"
                enabled: coeffsN.exists
                path: coeffsN.path
            }

            FoamValue {
                enabled: methodDropDown.currentText !== ""
                label: qsTr("Delta")
                path: "system/decomposeParDict " + methodDropDown.currentText + "Coeffs delta"
            }

            FoamDropDown {
                visible: methodDropDown.currentText === "hierarchical"
                label: qsTr("Order")

                modelPath: "decomposition hierarchicalOrders"
                path: "system/decomposeParDict hierarchicalCoeffs order"
            }
        }
    }
}
