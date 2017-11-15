import QtQuick.Layouts 1.3

import DICE.App 1.0
import DICE.App.Foam 1.0

SplitBody {
    AppLayoutCard {
        title: "Monitors"
        width: parent.width
        height: parent.height/2

        SimpleTreeView {
            id: cellZones
            Layout.fillHeight: true
            Layout.fillWidth: true
            model: app.monitoring.model
            delegate: SimpleTreeViewDelegate {
                contentSource: 'MonitorDelegate.qml'
            }
        }
    }

    TabsCard2 {
        title: qsTr("Properties")
        height: parent.height/2
        Layout.minimumHeight: 100
        Layout.preferredHeight: parent.height/2
        Layout.fillWidth: true
        Layout.fillHeight: true
        model: app.monitoring.properties
        delegateSource: "Props.qml"
        textRole: 'title'
    }
}
