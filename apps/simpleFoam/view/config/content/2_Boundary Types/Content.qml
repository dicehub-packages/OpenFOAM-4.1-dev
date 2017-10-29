import QtQuick.Layouts 1.3

import DICE.App 1.0

SplitBody {
    AppLayoutCard {
        title: "Boundaries"
        width: parent.width
        height: parent.height/2

        DiceInputField {
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
        model: app.boundaryPropsModel
        delegateSource: "Props.qml"
        textRole: 'modelData'
    }
}
