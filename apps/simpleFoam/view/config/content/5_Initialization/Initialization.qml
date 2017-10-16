import QtQuick 2.4

import DICE.App 1.0
import DICE.App.Foam 1.0

Column {

    Item {
        height: 20
        width: parent.width
    }

    ValueField {
        visible: modelData.modelData == "p - Pressure"
        path: "foam:0/p internalField %field"
    }
    VectorField {
        visible: modelData.modelData == "U - Velocity"
        path: "foam:0/U internalField %field_vector"
    }
    ValueField {
        visible: modelData.modelData == "k"
        path: "foam:0/k internalField %field"
    }
    ValueField {
        visible: modelData.modelData == "Omega"
        path: "foam:0/omega internalField %field"
    }
    ValueField {
        visible: modelData.modelData == "Epsilon"
        path: "foam:0/epsilon internalField %field"
    }
    ValueField {
        visible: modelData.modelData == "nut"
        path: "foam:0/nut internalField %field"
    }
}