import DICE.App 1.0

Body {
    Card {
        header: CenteredImage {
            height: 100
            color: "#7b1fa2"
            source: "images/simpleFoam.svg"
        }
        title: "Description"

        BodyText {
            text: "Steady-state solver for incompressible flows with turbulence modelling."
        }
    }
    Card {
        title: "Input"
        List {
            maxHeight: 300
            width: parent.width
            modelData: appController.input_types_model
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
            modelData: appController.output_types_model
            delegate: ListItem {
                text: output_type
            }
        }
    }
}
