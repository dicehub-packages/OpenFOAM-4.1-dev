import QtQuick.Controls 1.4
import QtQuick 2.5
import QtQml.Models 2.2
import QtQuick.Layouts 1.3

import DICE.App 1.0
import DICE.Components 1.0

Loader {
    width: parent.width
    height: !!item ? item.height : 0
    source: {
        switch (modelData.modelData) {
            case 'Time':
                return "Time.qml"
            case 'Gradients':
                return "Gradients.qml"
            case 'Interpolation':
                return "Interpolation.qml"
        }
    }
}

