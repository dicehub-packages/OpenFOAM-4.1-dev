import QtQuick 2.9

import DICE.App 1.0

Column {
    height: childrenRect.height
    width: parent.width

    ToggleButton {
        id: toggleParentLevel
        label: qsTr("Use parent level")
        path: "refinement:SurfaceRegion.parent_level"
    }

    DiceVectorField2D2 {
    	enabled: !toggleParentLevel.checked
        xLabel: "Min Level"
        yLabel: "Max Level"
        dataType: "int"
        path: "refinement:SurfaceRegion.surface_level"
    }
}
