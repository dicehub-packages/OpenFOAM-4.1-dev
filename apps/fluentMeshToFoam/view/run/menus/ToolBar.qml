import DICE.App 1.0
import DICE.Components 1.0 as DC

import QtQuick.Layouts 1.1
import QtQuick 2.7 as QQ

ToolBarMenu {
   ToolBarGroup {
       title: qsTr("Mesh tools")

       BigToolBarButton {
           diceIconName: "Mesh"
           text: "checkMesh options"
           onClicked: checkMeshDrawer.open()

           CheckMeshDrawer {
               id: checkMeshDrawer
           }
       }
   }
}
