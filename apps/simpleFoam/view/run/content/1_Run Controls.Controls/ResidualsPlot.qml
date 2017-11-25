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
                        setVisible(visible)
                    }
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                    Component.onCompleted: {
                        plot.parent = this;
                        plot.anchors.fill = this;
                        plot.width = root.width
                        plot.height = root.height
                    }
                }
            }
        }
    }
}
