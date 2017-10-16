import QtQuick 2.5
import DICE.App 1.0

import DICE.Components 1.0

Rectangle {
    id: root

    height: Math.max(text.implicitHeight, stepNumber.height)
    width: parent.width
    color: "transparent"
    
    Row {
        width: parent.width
        height: parent.height
        spacing: 15
        
        Rectangle {
            id: stepNumber
            
            width: 50
            height: 50
            radius: variables.componentBorderRadius
            border.width: 1
            border.color: colors.theme["base_border_color"]
            color: "transparent"
            
            SubheaderText {
                text: index
                anchors.centerIn: parent
                type: "subtle"
            }
        }
        Rectangle {
            width: parent.width - stepNumber.width - parent.spacing
            height: parent.height
            color: "transparent"
            
            BodyText {
                id: text
                anchors.fill: parent
                anchors.margins: 5
                text: stepDescription
                verticalAlignment: "AlignVCenter"
                font.letterSpacing: 1.1
            }
        }
    }
}
