import DICE.App 1.0

Body {
    TabsCard3 {
        title: qsTr("Discretization")
        model:  ["Convection", "Gradients", "Interpolation"]
        delegateSource: "Props.qml"
        textRole: 'modelData'
    }
}
