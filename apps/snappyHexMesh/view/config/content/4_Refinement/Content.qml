import QtQuick 2.4
import QtQuick.Layouts 1.3

import DICE.App 1.0
import DICE.Components 1.0

SplitBody {
    AppLayoutCard {
        id: tree
        title: qsTr("Geometry objects")
        height: parent.height/2
        Layout.minimumHeight: 100
        Layout.fillWidth: true
        Layout.fillHeight: true
        SimpleTreeView {
            Layout.fillHeight: true
            Layout.fillWidth: true
            height: 100
            width: parent.width
            model: app.refinement.model
            delegate: SimpleTreeViewDelegate {
                contentSource: 'RefinementListDelegate.qml'
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
        model: app.refinement.properties
        delegateSource: "Props.qml"
        textRole: 'title'
    }
}
