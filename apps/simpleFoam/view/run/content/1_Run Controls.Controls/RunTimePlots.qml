import QtQuick 2.9
import QtQuick.Controls 1.4 as QC1
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3

import DICE.App 1.0

Item {
    id: root

    Column {
        anchors.fill: parent

        TabBar {
            id: bar
            Layout.fillWidth: true
            width: parent.width

            Repeater {
                model: app.plots.model
                delegate: TabButton {
                    text: name
                }
            }
        }

        StackLayout {
            width: parent.width
            height: parent.height - bar.height
            currentIndex: bar.currentIndex

            Repeater {
                model: app.plots.model
                delegate: Item {
                    id: plotItem
                    onVisibleChanged: {
                        setVisible(visible)
                    }
                    width: parent.width
                    height: parent.height
                    Component.onCompleted: {
                        plot.parent = this
                        plot.anchors.fill = this
                    }
                }
            }
        }

//        Repeater  {
//            id: repeater
//            model: app.plots.model

//            property var currentItem

//            Loader {
//                id: loader

//                property bool activeTab: index === bar.currentIndex

//                Layout.fillHeight: true
//                Layout.fillWidth: true
//                onActiveTabChanged: {
//                    if (activeTab && item) {
//                        repeater.currentItem = item
//                        setVisible(true)
//                    }
//                    else {
//                        setVisible(false)
//                    }
//                    print("--active: ", item)
//                    print("--visible: ", visible)
//                }
//                visible: activeTab
//                sourceComponent: Item {
//                    Component.onCompleted: {
//                        plot.parent = this
//                        plot.anchors.fill = this
//                    }
//                }
//                onLoaded: {
//                    print("ITEM --->>>",item)
//                    if (index === 0) {
//                        repeater.currentItem = item
//                    }
//                }
//            }
//        }
    }
}
