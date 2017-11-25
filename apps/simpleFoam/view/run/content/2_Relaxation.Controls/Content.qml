import QtQuick 2.9
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.2

import DICE.App 1.0

SplitView {
    anchors.fill: parent
    Rectangle {
        Layout.fillHeight: true
        Layout.minimumWidth: 350
        width: parent.width/4
        color: colors.theme["app_background_color"]

        Body {
            Card {
                title: qsTr("Relaxation Factors")
                spacing: 20

                DiceValueField {
                    label: "Pressure"
                    path: "foam:system/fvSolution relaxationFactors fields p"
                }
                DiceValueField {
                    label: "Velocity"
                    path: "foam:system/fvSolution relaxationFactors equations U"
                }
                DiceValueField {
                    label: "k"
                    path: "foam:system/fvSolution relaxationFactors equations k"
                    visible: app.turbulenceModel === "kEpsilon" ||
                             app.turbulenceModel === "kOmegaSST"
                    enabled: visible
                }
                DiceValueField {
                    label: "Epsilon"
                    path: "foam:system/fvSolution relaxationFactors equations epsilon"
                    visible: app.turbulenceModel === "kEpsilon" ||
                             app.turbulenceModel === "kOmegaSST"
                    enabled: visible
                }
                DiceValueField {
                    label: "Omega"
                    path: "foam:system/fvSolution relaxationFactors equations omega"
                    visible: app.turbulenceModel === "kEpsilon" ||
                             app.turbulenceModel === "kOmegaSST"
                    enabled: visible
                }
            }
        }
    }

    Item {
        Layout.fillHeight: true
        Layout.fillWidth: true
    }
}
