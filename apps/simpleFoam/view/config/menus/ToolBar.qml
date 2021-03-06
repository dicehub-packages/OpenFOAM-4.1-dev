import QtQuick 2.4
import DICE.App 1.0
import DICE.Components 1.0 as DC

ToolBarMenu {

    ToolBarGroup {
        title: qsTr("Utilities")

        Row {
            width: childrenRect.width
            height: parent.height
            spacing: 5
            DC.BigToolBarButton {
                tooltip: "Check Mesh ..."
                diceIconName: "mesh"
                enabled: !mainWindow.current_app.running
                         && appController.progress !== 0
                         && appController.progress === -1
                onClicked: app.runCheckMesh()
                anchors.verticalCenter: parent.verticalCenter
                text: "Check Mesh"
            }
        }
    }
}
