import QtQuick 2.4

import DICE.App 1.0

ToolBarMenu {

    ToolBarGroup {
        title: qsTr("Refinement Objects")

        BigToolBarButton {
            iconSource: "images/refinementBox.svg"
            text: qsTr("Box")
            tooltip: qsTr("Add Refinement Box")
            onClicked: {
                app.refinement.addRefinementObject('refinementBox')
                appRoot.openTab("Refinement")
            }
        }

        BigToolBarButton {
            iconSource: "images/refinementSphere.svg"
            text: qsTr("Sphere")
            tooltip: qsTr("Add Refinement Sphere")
            onClicked: {
                app.refinement.addRefinementObject('refinementSphere')
                appRoot.openTab("Refinement")
            }
        }

        BigToolBarButton {
            iconSource: "images/refinementCylinder.svg"
            text: qsTr("Cylinder")
            tooltip: qsTr("Add Refinement Cylinder")
            onClicked: {
                app.refinement.addRefinementObject('refinementCylinder')
                appRoot.openTab("Refinement")
            }
        }

        BigToolBarButton {
            iconSource: "images/refinementPlate.svg"
            text: qsTr("Plate")
            tooltip: qsTr("Add Refinement Plate")
            onClicked: {
                app.refinement.addRefinementObject('refinementPlate')
                appRoot.openTab("Refinement")
            }
        }

        BigToolBarButton {
            iconSource: "images/refinementPlane3P.svg"
            text: qsTr("Plane (3 Points)")
            tooltip: qsTr("Add Refinement Plane by defining 3 Points")
            onClicked: {
                app.refinement.addRefinementObject('refinementPlane3P')
                appRoot.openTab("Refinement")
            }
        }

        BigToolBarButton {
            iconSource: "images/refinementPlanePaN.svg"
            text: qsTr("Plane (Point + Normal)")
            tooltip: qsTr("Add Refinement Plane by a Point and a Normal Vector")
            onClicked: {
                app.refinement.addRefinementObject('refinementPlanePaN')
                appRoot.openTab("Refinement")
            }
        }

        BigToolBarButton {
            iconSource: "images/refinementDisk.svg"
            text: qsTr("Disk")
            tooltip: qsTr("Add Refinement Disk")
            onClicked: {
                app.refinement.addRefinementObject('refinementDisk')
                appRoot.openTab("Refinement")
            }
        }
    }
}
