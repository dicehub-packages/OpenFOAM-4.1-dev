import QtQuick 2.9

import DICE.Components 1.0


DiceScrollView {
    id: scrollView
    width: parent.width
    Loader {
        width: scrollView.width-10
        height: !!item ? item.height : 0
        source: "FunctionObjectsProps/" + modelData.source
    }
}

