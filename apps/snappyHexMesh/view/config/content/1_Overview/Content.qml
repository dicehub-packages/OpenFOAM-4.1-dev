import QtQuick 2.5
import DICE.App 1.0
import QtQuick.Layouts 1.3

Body {
    Card {
        title: "Background colors"
        header: CenteredImage {
            height: 100
            color: "#D64F2F"
            source: "images/sHM_icon.png"
        }
        BodyText {
            width: parent.width
            text: app.shortDescription
        }
    }

    Card {
        title: "Example"
        FullWidthImage {
            source: "images/motorbike_sHM.png"
        }
        BodyText {
            text: "Mesh from Motorbike-Tutorial:"
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
