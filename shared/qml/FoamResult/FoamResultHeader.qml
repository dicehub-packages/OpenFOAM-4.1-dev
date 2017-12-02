import QtQuick 2.7
import QtQuick.Layouts 1.3
import QtQuick.Controls 1.4 as QC1
import QtQuick.Controls 2.1

import DICE.App 1.0
import DICE.Components 1.0 as DC

Rectangle {
    width: parent.width
    height: 50
    color: colors.theme["base_background_color"]
    
    DC.DiceScrollView {
        id: headerScrollView
        width: parent.width
        height: 50
        
        Row {
            id: headerRow
            height: parent.height
            spacing: 5

            ToggleButton {
                uncheckedText: "Manual range"
                checkedText: qsTr("Auto range")
                target: app.result
                property: "fieldRangeAuto"
                width: 200
            }

            DiceButton {
                width: 100
                text: "Custom Data Range"
                flat: true
                onClicked: {
                    customDataRangeDialog.open()
                }
                CustomDataRangeDialog {
                    id: customDataRangeDialog
                }
            }

            DiceComboBox {
                width: 200
                target: app.result
                property: "currentField"
                model: app.result.fieldNames
            }

            DiceComboBox {
                width: 70
                target: app.result
                property: "currentFieldComponent"
                model: app.result.currentFieldComponentNames
                enabled: model.length !== 0
            }

            DiceCheckBox {
                text: "Point data"
                onClicked: {
                    app.result.pointDataMode = checked
                }
                checked: app.result.pointDataMode
            }
        }
    }
    DC.BottomBorder {}
}
