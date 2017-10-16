import QtQuick 2.4
import QtQuick.Controls 1.2

Item {

    // Refinement Objects
    // ==================
    // property Action addBox: Action {
    //     text: qsTr("Box")
    //     tooltip: qsTr("Add Refinement Box")
    //     iconSource: "images/refinementBox.svg"
    //     iconName: text
    //     onTriggered:  {
    //         app.refinement.addRefinementObject('refinementBox')
    //         appRoot.openTab("Refinement")

    //         // app.call("add_refinement_object", ["refinementBox"], function(realObjName){treeView.setCurrentNode(realObjName)})
    //     }
    // }
    // property Action addSphere: Action {
    //     text: qsTr("Sphere")
    //     tooltip: qsTr("Add Refinement Sphere")
    //     iconSource: "images/refinementSphere.svg"
    //     iconName: text
    //     onTriggered:  {
    //         app.refinement.addRefinementObject('refinementSphere')
    //         appRoot.openTab("Refinement")
    //         // app.call("add_refinement_object", ["refinementSphere"], function(realObjName){treeView.setCurrentNode(realObjName)})
    //     }
    // }
    // property Action addCylinder: Action {
    //     text: qsTr("Cylinder")
    //     tooltip: qsTr("Add Refinement Cylinder")
    //     iconSource: "images/refinementCylinder.svg"
    //     iconName: text
    //     onTriggered:  {
    //         appRoot.openTab("Refinement")
    //         app.call("add_refinement_object", ["refinementCylinder"], function(realObjName){treeView.setCurrentNode(realObjName)})
    //     }
    // }
    // property Action addPlate: Action {
    //     text: qsTr("Plate")
    //     tooltip: qsTr("Add Refinement Plate")
    //     iconSource: "images/refinementPlate.svg"
    //     iconName: text
    //     onTriggered:  {
    //         appRoot.openTab("Refinement")
    //         app.call("add_refinement_object", ["refinementPlate"], function(realObjName){treeView.setCurrentNode(realObjName)})
    //     }
    // }
    // property Action addPlanePointAndNormal: Action {
    //     text: qsTr("Plane (Point + Normal)")
    //     tooltip: qsTr("Add Refinement Plane (Point + Normal)")
    //     iconSource: "images/refinementPlanePointAndNormal.svg"
    //     iconName: text
    //     onTriggered:  {
    //         appRoot.openTab("Refinement")
    //         app.call("add_refinement_object", ["refinementPlanePaN"], function(realObjName){treeView.setCurrentNode(realObjName)})
    //     }
    // }
    // property Action addPlane3Points: Action {
    //     text: qsTr("Plane (3 Points)")
    //     tooltip: qsTr("Add Refinement Plane (3 Points)")
    //     iconSource: "images/refinementPlane3Points.svg"
    //     iconName: text
    //     onTriggered:  {
    //         appRoot.openTab("Refinement")
    //         app.call("add_refinement_object", ["refinementPlane3P"], function(realObjName){treeView.setCurrentNode(realObjName)})
    //     }
    // }
    // property Action addDisk: Action {
    //     text: qsTr("Disk")
    //     tooltip: qsTr("Add Refinement Disk")
    //     iconSource: "images/refinementDisk.svg"
    //     iconName: text
    //     onTriggered:  {
    //         appRoot.openTab("Refinement")
    //         app.call("add_refinement_object", ["refinementDisk"], function(realObjName){treeView.setCurrentNode(realObjName)})
    //     }
    // }

    /// Decomposition / Parallel Run
    // ============================
    // DecompositionOptions { id: decompositionOptions }
    // property Action openDecompositionOptions: Action {
    //     text: qsTr("Decomposition Options")
    //     tooltip: qsTr("Open decomposition options for a parallel run")
    //     iconSource: "images/decomposition.svg"
    //     iconName: text
    //     onTriggered: {
    //         leftOptionsSideBar.content = decompositionOptions
    //         leftOptionsSideBar.open()
    //     }
    // }

    // Treeview
    // =========
    // property var treeView: appRoot.contentItems["Refinement"].treeView

    // property Action removeRefinementObject: Action {
    //     text: qsTr("Remove Refinement Object")
    //     tooltip: text
    //     iconName: text

    //     enabled: !!treeView && !!treeView.currentNode && treeView.currentNode.model.isRefinementObject
    //     onTriggered: app.call("remove_refinement_object", [treeView.currentNodePath[0]])
    // }

    // RenameDialog { id: renameDialog }
    // property Action renameRefinementObject: Action {
    //     text: qsTr("Rename refinement object")
    //     tooltip: text
    //     iconName: text

    //     enabled: !!treeView && !!treeView.currentNode && treeView.currentNode.model.isRefinementObject
    //     onTriggered: {
    //         leftOptionsSideBar.content = renameDialog
    //         leftOptionsSideBar.open()
    //     }
    // }

    // External Tools
    // ==============
    // property Action openParaview: Action {
    //     text: qsTr("Open Paraview")
    //     tooltip: text
    //     iconSource: "images/openParaview.svg"
    //     iconName: text
    //     onTriggered:  {
    //         app.call("open_paraview")
    //     }
    // }

    // Tools
    // =====

    // Mesh Tools
    // ==========
    // property Action runCheckMesh: Action {
    //     text: qsTr("Run checkMesh utility")
    //     tooltip: text
    //     iconName: text
    //     iconSource: "images/checkMesh.svg"

    //     enabled: app.status === "finished"
    //     onTriggered: {
    //         app.call("run_check_mesh")
    //     }
    // }


    // property Action runRenumberMesh: Action {
    //     text: qsTr("Run renumberMesh utility")
    //     tooltip: text
    //     iconName: text

    //     enabled: app.status === "finished"
    //     onTriggered: {
    //         app.call("run_renumber_mesh")
    //     }
    // }

    // property Action clearMesh: Action {
    //     text: qsTr("Clear Mesh")
    //     tooltip: text
    //     iconName: text

    //     enabled: app.status === "finished"
    //     onTriggered: {
    //         app.call("clear_mesh")
    //     }
    // }
}
