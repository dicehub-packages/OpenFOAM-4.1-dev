import QtQuick 2.9

import DICE.App 1.0


Column {
    spacing: 10
    width: parent.width
    height: childrenRect.height

    Subheader {
        text: "Forces Monitor Settings"
        horizontalAlignment: "AlignHCenter"
    }

    DiceButton {
        text: "Select Monitored Patches"
        enabled: canOpenSelectPatchesDialog.value
        visible: canOpenSelectPatchesDialog.value
        DiceValueConnector {
            id: canOpenSelectPatchesDialog
            path: "functionObjects:ForcesMonitor.can_open_select_patches_dialog"
        }
        onClicked: {
            monitoredPatchesDialog.open()
        }
        MonitoredPatchesDialog {
            id: monitoredPatchesDialog
        }
    }

    Subheader {
        text: "Centre of rotation"
    }
    DiceVectorField {
        path: "functionObjects:ForcesMonitor.cofr"
    }

    Subheader {
        text: "Pitch axis"
    }
    DiceVectorField {
        path: "functionObjects:ForcesMonitor.pitch_axis"
    }

    DiceValueField {
        label: "Density [kg/m³]"
        path: "functionObjects:ForcesMonitor.rho_inf"
    }
}
