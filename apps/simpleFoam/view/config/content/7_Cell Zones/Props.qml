import QtQuick 2.9

import DICE.Components 1.0


ScrollView_DICE {
    id: scrollView
    anchors.fill: parent
    Loader {
        width: scrollView.width - 10
        height: !!item ? item.height : 0
        source: {
            switch (modelData.modelData) {
                case 'MRF Properties':
                    return "MRFproperties.qml"
            }
        }
    }
}

