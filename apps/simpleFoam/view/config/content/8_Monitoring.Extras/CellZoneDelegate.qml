import QtQuick 2.9
import QtQuick.Layouts 1.3

import DICE.Components 1.0

Item {
    width: parent.width
    height: Math.max(25, buttonLabel.height + 20)

    RowLayout {
        width: parent.width
        height: 20
        anchors.verticalCenter: parent.verticalCenter

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
                    font.bold: selected
                    color: colors.theme["text_color"]
                }
            }
        }
    }
}
