import QtQuick 2.4
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.2

import DICE.App 1.0

SplitView {

    anchors.fill: parent
    Item {
        Layout.fillHeight: true
        width: parent.width/4

        Body {

            Card {

                title: qsTr("Control")
                spacing: 20
                DiceValueField {
                    label: "Start Time"
                    path: "foam:system/controlDict startTime"
                }

                DiceValueField {
                    label: "End Time"
                    path: "foam:system/controlDict endTime"
                }

                DiceValueField {
                    label: "Time Step"
                    path: "foam:system/controlDict deltaT"
                }

                DiceValueField {
                    label: "Write Interval"
                    path: "foam:system/controlDict writeInterval"
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

        // Rectangle {
        //     id: rendererBackground

        //     anchors.fill: parent
        //     color: "#eee"
        //     gradient: Gradient {
        //         GradientStop { position: 0.0; color: "#EEE"; }
        //         GradientStop { position: 0.8; color: "#E9E9E9"; }
        //         GradientStop { position: 1.0; color: "#C0C0C0"; }
        //     }
        // }

        // Item {
        //     anchors.fill: parent
        //     Component.onCompleted: {
        //         app.resultScene.parent = this
        //         app.resultScene.anchors.fill = this
        //     }

        // }

        // VisControlPanel {
        //     id: visControl
        //     scene: app.resultScene
        // }
    }
}



// Item {
//     id: root
//     anchors.fill: parent
//     SplitView {
//         anchors.fill: parent
//         Rectangle {
//             width: 200
//             height: parent.height
//             color: 'red'
//         }

//     }
// }
