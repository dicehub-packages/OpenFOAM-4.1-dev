import QtQuick 2.9 as QQ

import DICE.App 1.0

Body {
    Card {
        title: qsTr("Material Point Coordinates")

        DiceVectorField {
            xLabel: "X"
            yLabel: "Y"
            zLabel: "Z"
            target: app.materialPoint
            property: 'location'
        }
        QQ.Row {
            spacing: 10
            width: parent.width

            DiceButton {
                width: (parent.width - parent.spacing)/2
                text: qsTr("Select")
                onClicked: {
                    app.materialPoint.selectVisObject()
                }
            }
            DiceButton {
                width: (parent.width - parent.spacing)/2
                text: qsTr("Reset position")
                onClicked: {
                    app.materialPoint.resetToBoundingBox()
                }
            }
        }
    }
}
