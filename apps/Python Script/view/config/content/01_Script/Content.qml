
import QtQuick 2.4
import QtQuick.Layouts 1.3

import DICE.Components 1.0
import DICE.App 1.0

Body {
    Card {
        title: "Script"

        DiceButton {
            width: parent.width
            text: "Save script"
            onClicked: {
                app.saveRequest();
            }
        }

        DiceInputField {
            target: app
            property: 'inputType'
            label: 'Input type'
        }

        DiceInputField {
            target: app
            property: 'outputType'
            label: 'Output type'
        }


        DiceComboBox {
            id: behaviour
            target: app
            property: 'behaviour'
            label: 'Behaviour'
            model: [
                'normal',
                'loop'
            ]
        }

        DiceInputField {
            visible: behaviour.currentText === 'loop'
            target: app
            property: 'internalOutputType'
            label: 'Internal output type'
        }

        DiceInputField {
            visible: behaviour.currentText === 'loop'
            target: app
            property: 'internalInputType'
            label: 'Internal input type'
        }

    }
}

