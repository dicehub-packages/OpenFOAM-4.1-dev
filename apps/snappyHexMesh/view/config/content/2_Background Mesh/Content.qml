import QtQuick.Controls 1.4
import QtQuick 2.6

import DICE.App 1.0

Body {
    Card {
        title: "Bounding Box"
        VectorField {
            id: bbMin
            xLabel: "min X"
            yLabel: "min Y"
            zLabel: "min Z"
            target: app.boundingBox
            property: 'boundingBoxMin'
        }
        VectorField {
            id: bbMax
            xLabel: "max X"
            yLabel: "max Y"
            zLabel: "max Z"
            target: app.boundingBox
            property: 'boundingBoxMax'
        }
        Caption {
            text: qsTr("Additional spacing [%]")
        }
        VectorField {
            id: spacingInput
            xLabel: "Spacing X [%]"
            yLabel: "Spacing Y [%]"
            zLabel: "Spacing Z [%]"
            target: app.boundingBox
            property: 'additionalSpacing'           
        }
        FlatButton {
            width: parent.width
            text: qsTr("Calculate Automatically")
            onClicked: {
                app.boundingBox.calculateBoundingBox()
            }
        }
    }
    Card {
        title: "Cells"
        ToggleButton {
            id: toggleSizeOrNumber
            uncheckedText: "Number of Cells"
            checkedText: qsTr("Cells Size Δs [m]")
            target: app.boundingBox
            property: "sizeOrNumber"
        }
        VectorField {
            // readOnly: toggleSizeOrNumber.checked
            xLabel: "Cells in X"
            yLabel: "Cells in Y"
            zLabel: "Cells in Z"
            dataType: "int"
            target: app.boundingBox
            property: 'cellsNum'    
        }
        VectorField {
            // readOnly: !toggleSizeOrNumber.checked
            xLabel: "Δs in X [m]"
            yLabel: "Δs in Y [m]"
            zLabel: "Δs in Z [m]"
            target: app.boundingBox
            property: 'cellsSize'   
        }
    }
    // Card {
    //     title: qsTr("Boundaries")
    //     ListView {
    //         width: parent.width
    //         height: contentHeight
    //         model: app.boundingBox.boundariesModel
    //         // delegate: Text{text:'blahhhh';height: 80;width: parent.width}
    //         delegate: Row {
    //             height: 80
    //             width: parent.width
    //             BodyText{text:name;height: 80;width: parent.width/2}
    //             InputField {
    //                 width: parent.width/2
    //                 label: qsTr('Name')
    //                 text: name
    //                 floating: false
    //                 onEditingFinished: {
    //                     name = text;
    //                     text = Qt.binding(function() {return name});
    //                 }
    //                 onActiveFocusChanged: {
    //                     if (activeFocus)
    //                         app.boundingBox.highlightFace(index)
    //                 }
    //             }

                // DropDown {
                //     width: parent.width/2

                //     Component.onCompleted: {
                //         for (var i = 0; i < types.count; ++i) {
                //             if (types.get(i).text == type) {
                //                 currentIndex = i
                //                 break
                //             }
                //         }
                //     }
                //     // activeFocusOnPress: true
                //     onActiveFocusChanged: {
                //         if (activeFocus)
                //             app.boundingBox.highlightFace(index)
                //     }

                //     model: ListModel {
                //         id: types
                //         ListElement {
                //             text: qsTr("patch")
                //         }
                //         ListElement {
                //             text: qsTr("wall")
                //         }
                //         ListElement {
                //             text: qsTr("symmetryPlane")
                //         }
                //         ListElement {
                //             text: qsTr("symmetry")
                //         }
                //         ListElement {
                //             text: qsTr("empty")
                //         }
                //         ListElement {
                //             text: qsTr("wedge")
                //         }
                //         ListElement {
                //             text: qsTr("cyclic")
                //         }
                //         ListElement {
                //             text: qsTr("cyclicAMI")
                //         }
                //         ListElement {
                //             text: qsTr("processor")
                //         }
                //     }

                //     onCurrentIndexChanged: {
                //         type = types.get(currentIndex).text
                //     }
                // }
        //     }
        // }


//        TreeView {
//            id: boundaries
//            width: parent.width
//            model: PythonListModel {
//                loadMethod: "get_boundaries"
//                changedCallback: "boundariesChanged"
//            }
//        }
//        DropDown {
//            label: "Type"
//            getModelMethod: "boundary_types"
//            modelPath: !!boundaries.currentNode ? "constant/polyMesh/blockMeshDict boundary " + boundaries.currentNode.model.index + " type": undefined
//        }
    // }
}
