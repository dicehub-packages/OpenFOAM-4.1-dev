import QtQuick 2.7 as QQ

import DICE.App 1.0

Body {
    Card {
        title: "Conversion"

        FileElement {
            collapsed: true
            visible: app.sourcePath !== ""
        }
        QQ.Item {
            width: parent.width
            height: 10
        }
        Button {
            text: app.sourcePath === "" ? "Import" : "Overwrite"
            width: (parent.width - parent.spacing)/2
            anchors.right: parent.right
            onClicked: {
                fileDialog.open("import_msh", "Select 1 file for coneverison",
                                ["MSH File (*.msh)"], false)
            }
        }
    }
}
