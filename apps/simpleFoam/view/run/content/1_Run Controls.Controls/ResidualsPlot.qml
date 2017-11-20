import QtQuick 2.9
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.2

import DICE.App 1.0

Item {
    id: root

    Layout.fillHeight: true
    Layout.fillWidth: true

    Component {
        id: plotComponent
        Item {
            id: plotItem
            property var plot: undefined
            anchors.fill: parent
        }
    }


    Loader {
        anchors.fill: parent
        sourceComponent: plotComponent
        onLoaded: {
            if (Loader.Ready) {
                item.plot = app.plot
                app.plot.parent = item
                app.plot.anchors.fill = item
            }
        }
    }
    
//    Rectangle {
//        id: fig
//        color: "#eee"
//        gradient: Gradient {
//            GradientStop { position: 0.0; color: "#EEE"; }
//            GradientStop { position: 0.8; color: "#E9E9E9"; }
//            GradientStop { position: 1.0; color: "#C0C0C0"; }
//        }
        
//        anchors.fill: parent
//        Component.onCompleted: {
//            app.plot.parent = this;
//            app.plot.anchors.fill = this;
//        }
//    }
}
