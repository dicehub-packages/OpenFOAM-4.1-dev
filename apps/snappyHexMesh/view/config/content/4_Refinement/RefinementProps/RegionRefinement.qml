import QtQuick 2.9

import DICE.App 1.0

Column {
    width: parent.width
//    height: visible ? childrenRect.height : 0

    Subheader {
        text: "Region Mode"
    }

    DiceComboBox {
        id: dropDown
        path: "refinement:RegionRefinement.region_mode"
        modelPath: "refinement:RegionRefinement.region_modes_list"
    }

    DiceValueConnector {
        id: levelCount
        path: "refinement:RegionRefinement.levels_count"
    }

    DiceValueConnector {
        id: canAddLevel
        path: "refinement:RegionRefinement.can_add_level"
    }

    Repeater {
        model: levelCount.value
        delegate: Row {
            spacing: 10
            width: parent.width
            DiceVectorField2D2 {
                width: parent.width-30
                xLabel: "Distance [m]"
                yLabel: "Level"
                xDataType: "double"
                xEnabled: dropDown.currentText === "distance"
                yDataType: "int"
                path: "refinement:RegionRefinement.level."+index
            }
            DiceButton {
                width: 20
                anchors.verticalCenter: parent.verticalCenter
                text: "-"
                onClicked: {
                    app.refinement.removeRegionLevel(index)
                }
            }
        }
    }

    DiceButton {
        width: parent.width
        text: "Add level"
        enabled: canAddLevel.value
        onClicked: {
            app.refinement.addRegionLevel()
        }
    }
}


