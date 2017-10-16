import DICE.App 1.0
import DICE.Components 1.0 as DC

import QtQuick.Layouts 1.1
import QtQuick 2.7 as QQ

Drawer {
    id: checkMeshDrawer
    width: 0.2 * appWindow.width
    height: appWindow.height
    
    onOpened: card.forceActiveFocus()
    
    Card {
        id: card
        
        title: "CheckMesh tool"
        
        header: QQ.Rectangle {
            height: 40
            width: parent.width
            color: "transparent"
            DC.SubheaderText {
                text: appController.name
                anchors.centerIn: parent
            }
            
            DC.DiceIconButton {
                anchors.right: parent.right
                height: 40
                iconName: "Close"
                color: colors.theme["text_color_subtle"]
                flat: true
                onClicked: {
                    checkMeshDrawer.close()
                }
            }
        }
        
        Subheader {
            text: "Options"
        }

        ValueConnector {
            id: allGeometry
            path: "config:checkMesh.allGeometry"
        }
        CheckBox {

            text: "Include bounding box checks"
            checked: allGeometry.value
            onClicked: allGeometry.value = !allGeometry.value
        }
        ValueConnector {
            id: allTopology
            path: "config:checkMesh.allTopology"
        }
        CheckBox {
            text: "Include extra topology checks"
            checked: allTopology.value
            onClicked: allTopology.value = !allTopology.value

        }
        
        QQ.Keys.onReturnPressed: {
            button.clicked()
        }
    }
}
