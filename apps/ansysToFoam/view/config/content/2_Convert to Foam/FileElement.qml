import QtQuick 2.7
import QtQuick.Layouts 1.1

import DICE.Components 1.0

Column {
    id: root

    property bool collapsed: false

    width: parent.width
    height: collapsed ?
                button.height :
                button.height + content.height
    clip: true

    Behavior on height {
        NumberAnimation { duration: 100 }
    }
    CollapseButton {
        id: button

        text: app.ansFileName
        collapsed: root.collapsed
    }
    Column {
        id: content

        width: parent.width
        spacing: 20
        visible: !root.collapsed

        Item {
            width: 1
            height: 5
        }
        BodyText {
            text: "<b>Path:</b> " + app.sourcePath
            width: parent.width
        }
    }
}
