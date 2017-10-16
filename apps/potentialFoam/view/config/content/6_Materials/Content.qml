import DICE.App 1.0
import DICE.App.Foam 1.0

Body {
    FlatButton {
        text: qsTr('Select Material')
        onClicked: {
            app.selectMaterial();
        }
    }
}
