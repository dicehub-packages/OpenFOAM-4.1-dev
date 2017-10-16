import QtQuick.Controls 1.4
import QtQuick 2.5
import QtQml.Models 2.2
import QtQuick.Layouts 1.3

import DICE.App 1.0
import DICE.Components 1.0

Column {
    width: parent.width
    height: visible ? childrenRect.height : 0

    DropDown2 {
        id: dropDown
        label: qsTr("Region Mode")
        path: "refinement:RegionRefinement.region_mode"
        modelPath: "refinement:RegionRefinement.region_modes_list"
    }

    ValueConnector {
        id: levelCount
        path: "refinement:RegionRefinement.levels_count"
    }

    ValueConnector {
        id: canAddLevel
        path: "refinement:RegionRefinement.can_add_level"
    }

    Repeater {
        model: levelCount.value
        delegate: Row {
            spacing: 10
            width: parent.width
            VectorField2D2 {
                width: parent.width-30
                xLabel: "Distance [m]"
                yLabel: "Level"
                xDataType: "double"
                xEnabled: dropDown.currentText === "distance"
                yDataType: "int"
                path: "refinement:RegionRefinement.level."+index
            }
            FlatButton {
                width: 20
                anchors.verticalCenter: parent.verticalCenter
                text: "-"
                onClicked: {
                    app.refinement.removeRegionLevel(index)
                }
            }
        }
    }

    FlatButton {
        width: parent.width
        text: "Add level"
        enabled: canAddLevel.value
        onClicked: {
            app.refinement.addRegionLevel()
        }
    }
}


