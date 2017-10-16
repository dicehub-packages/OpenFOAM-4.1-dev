import QtQuick 2.7 as QQ

import DICE.App 1.0

Body {
    Card {
        header: QQ.Image {
            sourceSize.width: parent.width
            source: "images/icon.svg"
            height: 100
            fillMode: QQ.Image.PreserveAspectCrop
        }
        title: "Description"
        BodyText {
            text: "Converts a Fluent mesh (in ASCII format) to foam format including multiple region and region boundary."
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
