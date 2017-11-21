import QtQuick 2.9
import QtQuick.Controls 1.4 as QC1
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3

import DICE.App 1.0
import DICE.Components 1.0 as DC

import "../1_Run Controls.Controls"

QC1.SplitView {
    anchors.fill: parent
    Rectangle {
        Layout.fillHeight: true
        Layout.minimumWidth: 300
        width: parent.width/4
        color: colors.theme["app_background_color"]

        Body {
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
    }

//    Item {
//        Layout.fillHeight: true
//        Layout.fillWidth: true

//        ListModel {
//            id: plotsModel
//            ListElement {
//                name: "Residuals"
//            }
//            ListElement {
//                name: "Forces"
//            }
//            ListElement {
//                name: "Forces 1"
//            }
//        }
//        ColumnLayout {
//            anchors.fill: parent

//            TabBar {
//                id: bar
//                Layout.fillWidth: true
//                Repeater {
//                    model: app.plots.model
//                    delegate: TabButton {
//                        text: name
//                    }
//                }
//            }
//            StackLayout {
//                Layout.fillWidth: true
//                Layout.fillHeight: true
//                currentIndex: bar.currentIndex
//                Repeater {
//                    model: app.plots.model
//                    delegate: Item {
//                        id: root

//                        Layout.fillHeight: true
//                        Layout.fillWidth: true

//                        Component {
//                            id: plotComponent
//                            Item {
//                                id: plotItem
//                                property var plot: undefined
//                                anchors.fill: parent
//                            }
//                        }


//                        Loader {
//                            anchors.fill: parent
//                            sourceComponent: plotComponent
//                            onLoaded: {
//                                if (Loader.Ready) {
//                                    item.plot = plot
//                                    plot.parent = item
//                                    plot.anchors.fill = item
//                                }
//                            }
//                        }
//                    }
//                }
//            }
//        }
//    }
    ResidualsPlot {}
}
