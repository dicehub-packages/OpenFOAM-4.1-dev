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


       // BigToolBarButton {
       //     action: actions.addBox
       // }
       // BigToolBarButton {
       //     action: actions.addSphere
       // }
//        // BigToolBarButton {
//        //     action: actions.addCylinder
//        // }
//        // BigToolBarButton {
//        //     action: actions.addPlate
//        // }
//        // BigToolBarButton {
//        //     action: actions.addPlanePointAndNormal
//        // }
//        // BigToolBarButton {
//        //     action: actions.addPlane3Points
//        // }
//        // BigToolBarButton {
//        //     action: actions.addDisk
//        // }
   }

    // ToolBarGroup {
    //     title: qsTr("Decomposition / Parallel Run")

    //     BigToolBarButton {
    //         action: actions.openDecompositionOptions
    //     }
    // }

    // ToolBarGroup {
    //     title: qsTr("External Tools")
    //     BigToolBarButton {
    //         action: actions.openParaview
    //     }
    // }

    // ToolBarGroup {
    //     title: "Treeview"

    //     property var treeView: appRoot.contentItems["Refinement"].treeView

    //     visible: !!treeView && !!treeView.currentNode && treeView.currentNode.model.isRefinementObject
    //     flowLeftToRight: false

    //     SmallToolBarButton {
    //         action: actions.removeRefinementObject
    //     }
    //     SmallToolBarButton {
    //         action: actions.renameRefinementObject
    //     }
    // }

    // ToolBarGroup {
    //     title: qsTr("Mesh Tools")
    //     visible: app.status === "finished"

    //     flowLeftToRight: false

    //     SmallToolBarButton {
    //         action: actions.runCheckMesh
    //     }
    //     SmallToolBarButton {
    //         action: actions.runRenumberMesh
    //     }
    //     SmallToolBarButton {
    //         action: actions.clearMesh
    //     }
    // }
}
