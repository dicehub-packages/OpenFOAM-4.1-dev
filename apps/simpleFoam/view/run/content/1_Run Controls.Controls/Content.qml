import QtQuick 2.9
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.2

import DICE.App 1.0

SplitView {
    anchors.fill: parent
    Rectangle {
        Layout.fillHeight: true
        width: parent.width/4
        color: colors.theme["app_background_color"]

        Body {
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
    }


    Item {
        Layout.fillHeight: true
        Layout.fillWidth: true

        Rectangle {
            id: fig
            color: "#eee"
            gradient: Gradient {
                GradientStop { position: 0.0; color: "#EEE"; }
                GradientStop { position: 0.8; color: "#E9E9E9"; }
                GradientStop { position: 1.0; color: "#C0C0C0"; }
            }

            anchors.fill: parent
            Component.onCompleted: {
                app.plot.parent = this;
                app.plot.anchors.fill = this;
            }
        }
    }
}