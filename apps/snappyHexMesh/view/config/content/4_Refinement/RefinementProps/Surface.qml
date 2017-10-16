import QtQuick 2.5
import QtQuick.Controls 2.0
import DICE.App 1.0
import QtQuick.Controls.Material 2.0
import QtQuick.Controls.Styles 1.3
import QtQuick.Controls.Private 1.0


Column {
    
    spacing: 10
    height: childrenRect.height
    width: parent.width

    VectorField2D2 {
        xLabel: "Min Level"
        yLabel: "Max Level"
        dataType: "int"
        path: "refinement:Surface.surface_level"
    }

    ToggleButton {
        id: convertToRegion
        label: qsTr("Convert to Region")
        path: "refinement:Surface.is_region"
    }

    Column {
        spacing: 10
        enabled: convertToRegion.checked
        visible: enabled
        height: enabled ? childrenRect.height : 0
        width: parent.width

        DropDown2 {
            label: qsTr("Cell Zone")
            model: ["inside", "outside"]
            path: "refinement:Surface.cell_zone_inside"
        }

        DropDown2 {
            label: qsTr("Face Type")
            model: ["internal", "baffle", "boundary"]
            path: "refinement:Surface.face_type"
        }
    }
}
