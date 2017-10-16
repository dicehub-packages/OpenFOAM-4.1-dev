import QtQuick 2.5
import DICE.App 1.0

import DICE.Components 1.0

DiceScrollView {
    id: root

    Column {
        anchors.top: parent.top
        anchors.topMargin: 15
        width: root.width - 20
        anchors.horizontalCenter: parent.horizontalCenter
        spacing: 20

        property var stepsModel: ListModel {
            ListElement {
                stepDescription: "Place your geometry in to the workflow directory (for example: $WORKFLOW_DiR/resources).
                        This way you can share your workflow with your collegues."
            }
            ListElement {
                stepDescription: "Import your <b>geometry</b> in <b>CONVERT TO FOAM</b>-Tab on the left."
            }
            ListElement {
                stepDescription: "Select a <b>scaling factor</b> in the <b>SCALE</b>-Tab."
            }
            ListElement {
                stepDescription: "Switch to the <b>Run-View</b>."
            }
            ListElement {
                stepDescription: "Run App!"
            }
        }

        Repeater {
            model: parent.stepsModel
            Step {}
        }
    }
}
