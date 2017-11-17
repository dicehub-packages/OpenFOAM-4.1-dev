import QtQuick 2.9
import QtQuick.Layouts 1.3

import DICE.Components 1.0


Item {
    height: 20
    
    Connections {
        target: delegateRoot
        onDoubleClicked: showInScene()
    }

    RowLayout {
        width: parent.width
        height: 20
        anchors.verticalCenter: parent.verticalCenter

        Item {
            Layout.minimumWidth: 20
            height: 20
            anchors.verticalCenter: parent.verticalCenter
            property Component fileIcon: DiceFontAwesomeIcon {
                size: 12
                anchors.centerIn: parent
                name: "Folder"
            }
            property Component boundaryIcon: DiceIconSVG {
                source: "images/" + boundaryOrientation + ".svg"
                size: 16
            }
            property Component refinementObjectIcon: DiceIconSVG {
                source: "../../menus/images/" + templateName + ".svg"
                size: 16
            }
            Loader {
                anchors.centerIn: parent
                sourceComponent: {
                    if (boundaryOrientation != undefined){
                        return parent.boundaryIcon
                    }
                    if (type === "RefinementObject" && templateName != undefined) {
                        return parent.refinementObjectIcon
                    }

                    else {
                        return parent.fileIcon
                    }
                }
            }
        }

        BasicText {
            Layout.fillWidth: true
            anchors.margins: 5
            anchors.verticalCenter: parent.verticalCenter
            text: label //+ " [" + boundaryOrientation + "]"
        }

        Item {
            Layout.minimumWidth: 20
            height: 20
            anchors.verticalCenter: parent.verticalCenter

            property Component boundaryTypeIcon: DiceIconSVG {
                source: boundaryType !== undefined
                        ? "images/" + boundaryType + ".svg" :
                          ""
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
                    default:
                        return "#000"
                    }
                }
            }
            Loader {
                anchors.centerIn: parent
                sourceComponent: parent.boundaryTypeIcon
                enabled: boundaryType != undefined
            }
        }

        MouseArea {
            Layout.minimumWidth: 20
            height: 20
            anchors.verticalCenter: parent.verticalCenter
            enabled: type === "RefinementObject"
            visible: enabled
            cursorShape: "PointingHandCursor"

            DiceFontAwesomeIcon {
                size: 10
                anchors.centerIn: parent
                name: "Remove"
                color: colors.theme["text_color_info"]
            }
            onClicked: {
                remove()
            }
        }

        MouseArea {
            Layout.minimumWidth: 20
            height: 20
            anchors.verticalCenter: parent.verticalCenter
            enabled: isVisible !== undefined
            visible: enabled
            DiceFontAwesomeIcon {
                size: 12
                anchors.centerIn: parent
                name: isVisible ? "Eye" : "EyeSlash"
            }
            onClicked: {
                isVisible = ! isVisible
            }
        }

    }
}
