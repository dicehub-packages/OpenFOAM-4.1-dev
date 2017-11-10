import QtQuick.Layouts 1.3

import DICE.App 1.0
import DICE.App.Foam 1.0

SplitBody {
    AppLayoutCard {
        title: "Cell Zones"
        width: parent.width
        height: parent.height/2

        SimpleTreeView {
            id: cellZones
            Layout.fillHeight: true
            Layout.fillWidth: true
            model: app.cellZonesModel
            delegate: SimpleTreeViewDelegate {
                contentSource: 'CellZoneDelegate.qml'
            }
        }
    }

    TabsCard2 {
        title: qsTr("Properties")
        model: {
            if (!app.hasMrfProps) {
                return []
            }
            else {
                return ["MRF"]
            }
        }
        delegateSource: "Props.qml"
        textRole: 'modelData'
    }
}
