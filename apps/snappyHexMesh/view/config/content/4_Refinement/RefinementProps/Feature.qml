import QtQuick.Controls 1.4
import QtQuick 2.5
import QtQml.Models 2.2
import QtQuick.Layouts 1.3

import DICE.App 1.0


Column {
    width: parent.width
    height: childrenRect.height

    DiceSwitch {
        id: featureToggle
        text: qsTr("Add Feature")
        path: "refinement:Surface.has_feature"
    }

    Column {

        spacing: 10

        enabled: featureToggle.checked
        visible: enabled
        height: enabled ? childrenRect.height : 0
        width: parent.width

        Row {
            spacing: 10
            width: parent.width

            BodyText {
                width: (parent.width - parent.spacing)/2
                anchors.verticalCenter: parent.verticalCenter
                text: qsTr("Feature level")
                verticalAlignment: Text.AlignVCenter
            }

            DiceValueField {
                width: (parent.width - parent.spacing)/2
                label: ""
                path: "refinement:Surface.feature_level"
                dataType: 'int'
            }
        }

        Row {
            spacing: 10
            width: parent.width

            BodyText {
                width: (parent.width - parent.spacing)/2
                anchors.verticalCenter: parent.verticalCenter
                text: qsTr("includedAngle")
                verticalAlignment: Text.AlignVCenter
            }

            DiceValueField {
                width: (parent.width - parent.spacing)/2
                label: ""
                path: "refinement:Surface.included_angle"
            }
        }

        Subheader {
            text: "Extraction Method"
        }
        DiceComboBox {
            model: ["extractFromSurface"]
            path: "refinement:Surface.extraction_method"
        }

        DiceSwitch {
            text: qsTr("writeObj")
            path: "refinement:Surface.write_obj"
        }

        DiceSwitch {
            text: qsTr("nonManifoldEdges")
            path: "refinement:Surface.non_manifold_edges"
        }

        ToggleButton {
            label: qsTr("openEdges")
            path: "refinement:Surface.open_edges"
        }
    }
}
