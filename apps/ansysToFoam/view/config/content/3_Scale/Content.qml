import DICE.App 1.0

Body {
    Card {
        title: "Select a geometry scaling factor"

        Subheader {
            text: "Scale with"
        }
        RadioButton {
            text: "Meter [m] - 1.0"
            checked: app.scalingFactor === 1.0
            onClicked: app.scalingFactor = 1.0
        }
        RadioButton {
            text: "Centimetre [cm] - 1e-02"
            checked: app.scalingFactor === 0.01
            onClicked: app.scalingFactor = 0.01
        }
        RadioButton {
            text: "Millimetre [mm] - 1e-03"
            checked: app.scalingFactor === 0.001
            onClicked: app.scalingFactor = 0.001
        }
        RadioButton {
            id: other
            text: "Other"
        }
        ValueField {
            id: otherInput
            label: ""
            target: app
            property: 'scalingFactor'
            visible: other.checked
        }
    }
}
