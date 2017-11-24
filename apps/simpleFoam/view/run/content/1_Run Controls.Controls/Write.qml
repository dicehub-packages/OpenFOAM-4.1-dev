import QtQuick 2.9

import DICE.App 1.0

Column {
    width: parent.width
    spacing: 10

    Card {
        title: qsTr("Write Controls")
        spacing: 20

        DiceInlineComboBox {
            label: "Write Control"
            model: [
                "timeStep",
                "runTime",
                "adjustableRunTime",
                "cpuTime",
                "clockTime"
            ]
            path: "foam:system/controlDict writeControl"
        }
        DiceValueField {
            label: "Write Interval"
            path: "foam:system/controlDict writeInterval"
        }
        DiceValueField {
            label: "Purge Write"
            path: "foam:system/controlDict purgeWrite"
        }
        DiceInlineComboBox {
            label: "Write Control"
            model: [
                "ascii",
                "binary"
            ]
            path: "foam:system/controlDict writeFormat"
        }
        DiceValueField {
            label: "Write Precision"
            path: "foam:system/controlDict writePrecision"
            dataType: "int"
        }
        DiceSwitch {
            text: "Write Compression"
            path: "foam:system/controlDict writeCompression"
        }
        DiceInlineComboBox {
            label: "Time Format"
            model: [
                "fixed",
                "scientific",
                "general"
            ]
            path: "foam:system/controlDict timeFormat"
        }
        DiceInlineComboBox {
            label: "Graph Format"
            model: [
                "raw",
                "gnuplot",
                "xmgr",
                "jplot"
            ]
            path: "foam:system/controlDict graphFormat"
        }
    }
}
