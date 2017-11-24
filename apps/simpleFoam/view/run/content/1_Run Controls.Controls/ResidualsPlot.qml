import QtQuick 2.9
import QtQuick.Controls 1.4 as QC1
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3

import DICE.App 1.0

Item {
    id: root

    Layout.fillHeight: true
    Layout.fillWidth: true

    ColumnLayout {
        anchors.fill: parent

        TabBar {
            id: bar
            Layout.fillWidth: true
            Repeater {
                model: app.plots.model
                delegate: TabButton {
                    text: name
                }
            }
        }

        StackLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            currentIndex: bar.currentIndex

            Repeater {
                model: app.plots.model
                delegate: Item {
                    onVisibleChanged: {
                        print(visible)
                        setVisible(visible)
                    }
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                    Component.onCompleted: {
                        plot.parent = this;
                        plot.anchors.fill = this;
                        plot.width = 200
                        plot.height = 200
                    }
                }
            }
        }

//            GridView {
//                id: grid
//                Layout.fillWidth: true
//                Layout.fillHeight: true
////                currentIndex: bar.currentIndex

//                cellWidth: parent.width/4
//                cellHeight: parent.height/2

////                Repeater {
//                    model: app.plots.model
//                    delegate: Item {
//                        id: root

////                        Layout.fillHeight: true
////                        Layout.fillWidth: true

//                        width: grid.cellWidth*0.8
//                        height: grid.cellHeight*0.8

//                        Rectangle {
//                            id: fig
//                            color: "#eee"
//                            gradient: Gradient {
//                                GradientStop { position: 0.0; color: "#EEE"; }
//                                GradientStop { position: 0.8; color: "#E9E9E9"; }
//                                GradientStop { position: 1.0; color: "#C0C0C0"; }
//                            }

//                            anchors.fill: parent
//                            Component.onCompleted: {
//                                plot.parent = this;
//                                plot.anchors.fill = this;
////                                plot.width = 200
////                                plot.height = 200
//                            }
////                            implicitWidth: 200
////                            implicitHeight: 200
//                        }

//////                        Component {
//////                            id: plotComponent
////                            Item {
////                                id: plotItem
////                                property var plot: undefined
////                                anchors.fill: parent
////                            }
//////                        }


////                        Loader {
////                            anchors.fill: parent
////                            sourceComponent: plotComponent
////                            onLoaded: {
////                                if (Loader.Ready) {
////                                    item.plot = plot
////                                    plot.parent = item
////                                    plot.anchors.fill = item
////                                }
////                            }
////                        }
////                    }
//                }
//            }
    }
}
