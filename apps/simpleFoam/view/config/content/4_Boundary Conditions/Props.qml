import QtQuick.Controls 1.4
import QtQuick 2.5
import QtQml.Models 2.2
import QtQuick.Layouts 1.3

import DICE.App 1.0
import DICE.Components 1.0

ScrollView_DICE {
    id: scrollView
    anchors.fill: parent
    Loader {
        width: scrollView.width - 10
        height: !!item ? item.height : 0
        source: {
            switch (modelData.modelData) {
                case 'Pressure':
                    return "Pressure.qml"
                case 'Velocity':
                    return "Velocity.qml"
                case 'k':
                    return "K.qml"
                case 'Epsilon':
                    return "Epsilon.qml"
                case 'Omega':
                    return "Omega.qml"
            }
        }
    }
}

