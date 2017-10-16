import DICE.App 1.0
import DICE.App.Foam 1.0

Body {
    Card {
        title: "Material"

        spacing: 20

        FlatButton {
            text: qsTr('Select Material')
            onClicked: {
                app.selectMaterial();
            }
        } 

        InputField2 {
            label: "nu"
            path: "foam:constant/transportProperties nu 2"
        }

    }

}
