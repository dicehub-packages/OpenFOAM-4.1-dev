import QtQuick 2.9
import QtQuick.Layouts 1.3

import DICE.Components 1.0

Item {
    width: parent.width
    height: 20

    RowLayout {
        width: parent.width
        height: 20
        anchors.verticalCenter: parent.verticalCenter

        DiceIconSVG {
            source: "images/" + boundaryType + ".svg"
            size: 16
            color: {
                switch (boundaryType) {
                case "patch":
                    return "#00007f"
                case "wall":
                    return "#000"
                case "symmetryPlane":
                    return "#5500ff"
                case "symetry":
                    return "#005500"
                case "empty":
                    return "#aaaaff"
                case "wedge":
                    return "#550000"
                }
            }
        }

        BasicText {
            Layout.fillWidth: true
            anchors.margins: 5
            anchors.verticalCenter: parent.verticalCenter
            text: name
        }

        MouseArea {
            Layout.minimumWidth: 20
            height: 20
            anchors.verticalCenter: parent.verticalCenter
            enabled: isVisible !== undefined
            visible: enabled
            FontAwesomeIcon {
                size: 12
                anchors.centerIn: parent
                name: isVisible ? "Eye" : "EyeSlash"
            }
            onClicked: {
                isVisible =! isVisible
            }
        }
    }
}
