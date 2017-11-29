import QtQuick 2.7
import QtQuick.Controls 2.0

import DICE.App 1.0
import DICE.Components 1.0 as DC

DC.DiceDialog {
    id: root
    title: "Rescale to custom data range"
    
    parent: appWindow.overlay
    
    x: Math.round((appWindow.width - width) / 2)
    y: Math.round(appWindow.height / 6)
    width: Math.round(Math.min(appWindow.width, appWindow.height) / 3 * 2)
    modal: true
    focus: true
    
    contentItem: Column {
        width: parent.width
        height: parent.height
        
        DiceVectorField2D2 {
            width: parent.width
            xLabel: "Min"
            yLabel: "Max"
            target: app.result
            property: "fieldRange"
        }
        
        Row {
            width: parent.width
            spacing: 10
            
            Item {
                width: parent.width/2 - spacing/2
                height: parent.height
            }
            DiceButton {
                id: confirmButton
                
                width: parent.width/2 - spacing/2
                text: qsTr("Close")
                onClicked: {
                    root.accept()
                }
            }
        }
    }
    Keys.onReturnPressed: {
        confirmButton.clicked()
    }
    Keys.onEscapePressed: {
        cancelButton.clicked()
    }
}
