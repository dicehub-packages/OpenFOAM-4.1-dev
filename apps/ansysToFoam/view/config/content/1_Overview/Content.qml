import QtQuick 2.7 as QQ

import DICE.App 1.0

Body {
    Card {
        header: QQ.Image {
            sourceSize.width: parent.width
            source: "images/ansysToFoam.svg"
            height: 100
            fillMode: QQ.Image.PreserveAspectCrop
        }
        title: "Description"
        BodyText {
            text: "Converts an ANSYS input mesh file, exported from I-DEAS,
    to OpenFOAM format."
        }
    }
    Card {
        title: "Input"
        List {
            maxHeight: 300
            width: parent.width
            modelData: app.input_types_model
            delegate: ListItem {
                text: input_type
            }
        }
    }
    Card {
        title: "Output"
        List {
            maxHeight: 300
            width: parent.width
            modelData: app.output_types_model
            delegate: ListItem {
                text: output_type
            }
        }
    }
}
