import QtQuick 2.5
import QtQuick.Controls 2.0
import DICE.App 1.0
import QtQuick.Controls.Material 2.0
import QtQuick.Controls.Styles 1.3
import QtQuick.Controls.Private 1.0

Column {
    height: childrenRect.height
    width: parent.width

    DiceSwitch {
        id: addLayersSwitch
        text: qsTr("Add Layers")
        path: "refinement:SurfaceRegion.has_layers_addition"
    }

    DiceValueField {
        enabled: addLayersSwitch.checked
        width: parent.width
        label: qsTr("Number of Layers")
        path: "refinement:SurfaceRegion.layers_addition"
        dataType: "int"
    }
}
