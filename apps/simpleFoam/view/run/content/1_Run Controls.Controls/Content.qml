import QtQuick 2.9
import QtQuick.Controls 1.4 as QC1
import QtQuick.Layouts 1.3

import DICE.App 1.0


QC1.SplitView {
    anchors.fill: parent
    Rectangle {
        id: controls

        Layout.fillHeight: true
        Layout.minimumWidth: 350
        width: parent.width/4
        color: colors.theme["app_background_color"]
        Body {
            TabsCard3 {
                title: "Controls"
                model: ["Run", "Write"]
                delegateSource: "Props.qml"
                textRole: "modelData"
            }
        }
    }
    RunTimePlots {
        width: parent.width - controls.width
        height: parent.height
    }
}
