import QtQuick 2.9
//import QtQuick.Controls 1.4
//import QtQml.Models 2.2
//import QtQuick.Layouts 1.3

//import DICE.App 1.0
import DICE.Components 1.0

ScrollView_DICE {
    id: scrollView
    anchors.fill: parent
    Loader {
        width: scrollView.width - 10
        height: !!item ? item.height : 0
        source: {
            switch (modelData.modelData) {
                case 'boundary':
                    return "BoundaryProps.qml"
                case 'group':
                    return "GroupProps.qml"
            }
        }
    }
}

