import QtQuick 2.7
import QtQuick.Layouts 1.3
import QtQuick.Controls 1.4

import DICE.App 1.0

SplitView {
    anchors.fill: parent

    AppLayoutCard {
        Layout.fillHeight: true
        width: parent.width/4
        title: qsTr("Patches")

        SimpleTreeView {
            Layout.fillHeight: true
            Layout.fillWidth: true
            model: app.result.model
            delegate: SimpleTreeViewDelegate {
                contentSource: 'ResultDelegate.qml'
            }
        }
    }

    Item {
        Layout.fillHeight: true
        Layout.fillWidth: true

        Rectangle {
            id: rendererBackground

            anchors.fill: parent
            color: "#eee"
            gradient: Gradient {
                GradientStop { position: 0.0; color: "#EEE"; }
                GradientStop { position: 0.8; color: "#E9E9E9"; }
                GradientStop { position: 1.0; color: "#C0C0C0"; }
            }
        }

        Item {
            anchors.fill: parent
            Component.onCompleted: {
                app.result.scene.parent = this
                app.result.scene.anchors.fill = this
            }

        }

        VisControlPanel {
            id: visControl
            scene: app.result.scene
        }

        Column {

            anchors.margins: 20

            Subheader {
                text: "Field"
            }
            DiceComboBox {
                width: 200
                target: app.result
                property: "currentField"
                model: app.result.fieldNames
            }

            ToggleButton {
                id: toggleSizeOrNumber
                uncheckedText: "Manual range"
                checkedText: qsTr("Auto range")
                target: app.result
                property: "fieldRangeAuto"
            }

            DiceVectorField2D2 {
                height: 30
                xLabel: "Min"
                yLabel: "Max"
                target: app.result
                property: "fieldRange"
            }
        }


    }
}
