import QtQuick 2.9

import DICE.App 1.0
//import DICE.App.Foam 1.0

Column {

    Item {
        height: 20
        width: parent.width
    }

    DiceValueField {
        visible: modelData.modelData === "p - Pressure"
        path: "foam:0/p internalField %field"
    }
    DiceVectorField {
        visible: modelData.modelData === "U - Velocity"
        path: "foam:0/U internalField %field_vector"
    }
    DiceValueField {
        visible: modelData.modelData === "k"
        path: "foam:0/k internalField %field"
    }
    DiceValueField {
        visible: modelData.modelData === "Omega"
        path: "foam:0/omega internalField %field"
    }
    DiceValueField {
        visible: modelData.modelData === "Epsilon"
        path: "foam:0/epsilon internalField %field"
    }
    DiceValueField {
        visible: modelData.modelData === "nut"
        path: "foam:0/nut internalField %field"
    }
}
