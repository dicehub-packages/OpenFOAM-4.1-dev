import DICE.App 1.0
import DICE.Components 1.0

ToolBarMenu {
   ToolBarGroup {
       title: qsTr("This is main group")
       DiceSwitch {
           width: 150
           text: qsTr("Some main switch")
       }
   }
}
