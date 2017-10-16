import QtQuick 2.5
import QtQuick.Controls 2.0
import DICE.App 1.0
import QtQuick.Controls.Material 2.0
import QtQuick.Controls.Styles 1.3
import QtQuick.Controls.Private 1.0

Column {
    height: childrenRect.height
    width: parent.width

    ToggleButton {
        id: toggleParentLevel
        label: qsTr("Use parent level")
        path: "refinement:SurfaceRegion.parent_level"
    }

    VectorField2D2 {
    	enabled: !toggleParentLevel.checked
        xLabel: "Min Level"
        yLabel: "Max Level"
        dataType: "int"
        path: "refinement:SurfaceRegion.surface_level"
    }
}
