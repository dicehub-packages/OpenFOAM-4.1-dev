import QtQuick 2.9
import QtQuick.Layouts 1.1

import DICE.App 1.0
import DICE.Components 1.0 as DC


Column {
    spacing: 10
    width: parent.width
    height: childrenRect.height

    Subheader {
        text: "Rotating Frame (Multiple Reference Frame)"
    }

    DiceCheckBox {
        id: enableMrfCheckBox
        Layout.fillWidth: true
        text: "Enable MRF"
        checked: app.mrfIsEnabled
        onClicked: {
            app.mrfIsEnabled = !app.mrfIsEnabled
        }
    }

    Column {
        width: parent.width
        enabled: enableMrfCheckBox.checked
        visible: enabled

        Subheader {
            text: "Origin"
        }
        DiceVectorField {
            path: "mrf:origin"
        }
        Subheader {
            text: "Axis"
        }
        DiceVectorField {
            path: "mrf:axis"
        }
        Subheader {
            text: "Rotational Speed"
        }
        DiceValueField {
            label: "Omega [1/s]"
            path: "mrf:omega"
        }
        DiceSwitch {
            text: "Active"
            path: "mrf:active"
        }
        DiceButton {
            text: "Select Non Rotating Patches"
            enabled: app.singleCellZoneSelection
            visible: app.singleCellZoneSelection
            onClicked: {
                app.loadNonRotatingPatchesModel()
                nonRotatingPatchesDialog.open()
            }
            NonRotatingPatchesDialog {
                id: nonRotatingPatchesDialog
            }
        }
    }
}
