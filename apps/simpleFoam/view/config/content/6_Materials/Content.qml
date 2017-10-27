import DICE.App 1.0
import DICE.App.Foam 1.0

Body {
    Card {
        title: "Material"

        spacing: 20

        DiceButton {
            text: qsTr('Select Material')
            onClicked: {
                app.selectMaterial();
            }
        } 

        DiceInputField {
            label: "nu"
            path: "foam:constant/transportProperties nu 2"
        }

    }

}
