import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.1

import DICE.Components 1.0


Item {
    id: root
    property bool isCurrent: ListView.isCurrentItem

    width: ListView.view.width
    height: Math.max(25, buttonLabel.height + 20)
    clip: true

    onIsCurrentChanged: {
        isCurrent ? state = "ACTIVE" : state = "NORMAL";
    }

    Component.onCompleted: {
        isCurrent ? state = "ACTIVE" : state = "NORMAL"
    }

    Behavior on height {
        NumberAnimation {
            duration: 100
        }
    }

    Rectangle {
        id: background

        color: colors.theme["base_background_color"]
        anchors.fill: parent

        LeftBorder {
            color: colors.theme["button_background_color_selected"]
            anchors.leftMargin: 1
            width: 2
            visible: isCurrent
        }
        TopBorder {
            visible: isCurrent
        }
        BottomBorder {
            visible: isCurrent
        }
        RightBorder {
            visible: isCurrent
        }
    }

    Item {
        id: label

        anchors.fill: parent
        implicitHeight: col.height
        height: implicitHeight
        width: buttonLabel.width + 20

        Column {
            id: col

            spacing: 2
            anchors.verticalCenter: parent.verticalCenter

            BasicText {
                id: buttonLabel
                width: root.width - 60
                verticalAlignment: Text.AlignVCenter
                anchors {
                    left: parent.left
                    leftMargin: 10
                    rightMargin: 10
                }
                text: name
                font.bold: isCurrent
                color: colors.theme["text_color"]
            }
        }
    }

    MouseArea {
        id: mouseArea

        property int currentMouseX
        property int currentMouseY

        anchors.fill: parent
        hoverEnabled: true
        cursorShape: "PointingHandCursor"
        opacity: parent.containsMouse ? 1 : 0.7
        onEntered: {
            !isCurrent ? parent.state = "HOVER" : parent.state = "ACTIVE";
        }
        onExited: {
            !isCurrent ? parent.state = "NORMAL" : parent.state = "ACTIVE";
        }
        onClicked: {
            interpolationSchemesList.currentIndex = index
            currentInterpolationSchemeListIndex = index
            parent.forceActiveFocus()
        }
    }

    states: [
        State {
            name: "NORMAL"
            PropertyChanges {
                target: background
//                color: colors.theme["base_background_color"]
                color: "transparent"
            }
            PropertyChanges {
                target: buttonLabel
                color: colors.theme["text_color_subtle"]
            }
        },
        State {
            name: "HOVER"
            PropertyChanges {
                target: background
                color: colors.theme["background_color_highlight"]
            }
            PropertyChanges {
                target: buttonLabel
                color: colors.theme["text_color_highlight"]
            }
        },
        State {
            name: "ACTIVE"
            PropertyChanges {
                target: background
                color: colors.theme["background_color_selected"]
            }
            PropertyChanges {
                target: buttonLabel
                color: colors.theme["text_color_selected"]
            }
        }
    ]

    transitions: [
        Transition {
            from: "HOVER"; to: "ACTIVE"
            ColorAnimation {
                target: background
                properties: "color"
                duration: 300
            }
            ColorAnimation {
                target: buttonLabel
                properties: "color"
                duration: 300
            }
        }
    ]
}
