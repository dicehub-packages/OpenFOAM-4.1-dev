import QtQuick 2.9

Loader {
    width: parent.width
    height: !!item ? item.height : 0
    source: {
        switch (modelData.modelData) {
            case 'Convection':
                return "Convection.qml"
            case 'Gradients':
                return "Gradients.qml"
            case 'Interpolation':
                return "Interpolation.qml"
        }
    }
}

