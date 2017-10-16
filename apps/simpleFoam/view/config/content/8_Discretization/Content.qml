import QtQuick 2.4
import QtQuick.Layouts 1.3
import QtQuick.Controls 1.4

import DICE.App 1.0
import DICE.Components 1.0

Body {
    TabsCard3 {
        title: qsTr("Discretization")
        model:  ["Convection", "Gradients", "Interpolation"]
        delegateSource: "Props.qml"
        textRole: 'modelData'
    }
}
