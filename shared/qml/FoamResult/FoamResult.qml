import QtQuick 2.7
import QtQuick.Layouts 1.3
import QtQuick.Controls 1.4

import DICE.App 1.0
import DICE.Components 1.0 as DC

SplitView {
    anchors.fill: parent

    AppLayoutCard {
        Layout.fillHeight: true
        Layout.minimumWidth: 350
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

        DiceSwitch {
            id: autoLoadResultsSwitch
            Layout.fillWidth: true
            text: "Automatically load results"
            path: "config:autoLoadResult"
        }
        DiceButton {
            Layout.fillWidth: true
            text: "Load results"
            onClicked: {
                app.result.update()
            }
            enabled: !app.result.resultLoaded
            DC.DiceProgressBar {
                width: parent.width
                indeterminate: app.result.resultIsLoading
                visible: app.result.resultIsLoading
            }
        }
    }

    Column {
        Layout.fillHeight: true
        Layout.fillWidth: true

        Rectangle {
            id: header
            width: parent.width
            height: 50
            color: colors.theme["base_background_color"]

            Row {
                width: parent.width
                height: parent.height
                spacing: 5

                ToggleButton {
                    uncheckedText: "Manual range"
                    checkedText: qsTr("Auto range")
                    target: app.result
                    property: "fieldRangeAuto"
                    width: 200
                }

                DiceButton {
                    width: 100
                    text: "Custom Data Range"
                    flat: true
                    onClicked: {
                        customDataRangeDialog.open()
                    }
                    CustomDataRangeDialog {
                        id: customDataRangeDialog
                    }
                }

                DiceComboBox {
                    width: 200
                    target: app.result
                    property: "currentField"
                    model: app.result.fieldNames
                }

                DiceComboBox {
                    width: 70
                    target: app.result
                    property: "currentFieldComponent"
                    model: app.result.currentFieldComponentNames
                    enabled: model.length !== 0
                }

//                DiceButton {
//                    width: 100
//                    text: "test"
//                    onClicked: app.result.testFunction()
//                }
            }
            DC.BottomBorder {}
        }

        Item {
            width: parent.width
            height: parent.height - header.height

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
                id: renderItem
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

    //            Subheader {
    //                text: "Field"
    //            }


//                ToggleButton {
//                    id: toggleSizeOrNumber
//                    uncheckedText: "Manual range"
//                    checkedText: qsTr("Auto range")
//                    target: app.result
//                    property: "fieldRangeAuto"
//                }

//                DiceVectorField2D2 {
//                    height: 30
//                    xLabel: "Min"
//                    yLabel: "Max"
//                    target: app.result
//                    property: "fieldRange"
//                }
            }
        }
    }
}
