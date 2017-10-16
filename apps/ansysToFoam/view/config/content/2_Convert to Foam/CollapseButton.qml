import QtQuick 2.7
import QtQuick.Layouts 1.1

import DICE.Components 1.0


Rectangle {
    id: button

    property alias text: text.text
    property bool hovered: false
    property bool collapsed
    signal clicked

    color: hovered ?
               colors.theme["background_color_highlight"] :
               colors.theme["base_background_color"]
    height: text.paintedHeight*3
    width: parent.width

    Behavior on color {
        ColorAnimation { duration: 200 }
    }

    Row {
        width: parent.width - deleteButton.width
        height: parent.height

        FontAwesomeIcon {
            name: "AngleRight"
            color: colors.theme["text_color"]
            width: parent.height
            height: parent.height
            size: 10
            anchors.verticalCenter: parent.verticalCenter
            rotation: root.collapsed ? 0 : 90
            Behavior on rotation {
                NumberAnimation { duration: 50 }
            }
        }
        TitleText {
            id: text

            scalablePixelSize: 30
            verticalAlignment: "AlignVCenter"
            height: parent.height
        }
    }
    MouseArea {
        anchors.fill: parent
        onClicked: {
            if (!root.collapsed) {
                root.height = button.height
                root.collapsed = true
            }
            else {
                root.height = button.height
                        + content.height
                root.collapsed = false
            }
            forceActiveFocus()
        }
        hoverEnabled: true
        cursorShape: "PointingHandCursor"
        onEntered: {
            parent.hovered = !parent.hovered
        }
        onExited: {
            parent.hovered = !parent.hovered
        }
    }
    DiceIconButton {
        id: deleteButton
        iconName: "Delete"
        anchors.right: parent.right
        anchors.verticalCenter: parent.verticalCenter
        flat: true
        height: parent.height

        onClicked: {
            app.deleteImport()
        }
    }
}
