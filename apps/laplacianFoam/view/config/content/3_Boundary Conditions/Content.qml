import QtQuick 2.4
import QtQuick.Layouts 1.3
import QtQuick.Controls 1.4

import DICE.App 1.0
import DICE.Components 1.0

SplitBody {

    AppLayoutCard {
        title: "Boundaries"
        width: parent.width
        height: parent.height/2
        InputField {
            id: filterKeyword
            Layout.fillWidth: true
            label: "Filter"
            onTextChanged: {
                app.filterBoundaries(text)
            }
        }
        
        SimpleTreeView {
            id: boundaries
            Layout.fillHeight: true
            Layout.fillWidth: true
            model: app.boundariesModel
            delegate: SimpleTreeViewDelegate {
                contentSource: 'BoundaryDelegate.qml'
            }
        }
    }

    TabsCard2 {
        title: qsTr("Properties")
        model: app.hasProps ? ["Temperature"] : []
        delegateSource: "Props.qml"
        textRole: 'modelData'
    }
}
