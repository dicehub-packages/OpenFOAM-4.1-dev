import QtQuick 2.9

import DICE.App 1.0

Column {
    width: parent.width
    spacing: 10

    Card {
        title: qsTr("Run Controls")
        spacing: 20

        DiceInlineComboBox {
            id: stopFromComboBox
            label: "Start From"
            model: [
                "firstTime",
                "startTime",
                "latestTime"
            ]
            path: "foam:system/controlDict startFrom"
        }
        DiceValueField {
            label: "Start Time"
            path: "foam:system/controlDict startTime"
            enabled: stopFromComboBox.value === "startTime"
        }
        DiceValueField {
            label: "End Time"
            path: "foam:system/controlDict endTime"
            enabled: stopAtComboBox.value === "endTime"
        }
        DiceValueField {
            label: "Time Step"
            path: "foam:system/controlDict deltaT"
        }
        DiceInlineComboBox {
            id: stopAtComboBox
            label: "Stop At"
            model: [
                "endTime",
                "writeNow",
                "noWriteNow",
                "nextWrite"
            ]
            path: "foam:system/controlDict stopAt"
        }
    }
    Card {
        title: qsTr("Additional Write Controls")
        spacing: 20

        DiceValueField {
            label: "Write Interval"
            path: "foam:system/controlDict writeInterval"
        }
        DiceValueField {
            label: "Purge Write"
            path: "foam:system/controlDict purgeWrite"
        }
    }
}
