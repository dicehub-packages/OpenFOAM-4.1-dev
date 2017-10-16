import QtQuick 2.4

import DICE.App 1.0
import DICE.App.Foam 1.0

Body {
    Card {
        title: "Pressure [Pa]"
        ValueField {
            path: "foam:0/p internalField %field"
        }
    }
    Card {
        title: "Velocity [m/s]"
        VectorField {
            path: "foam:0/U internalField %field_vector"
        }
    }
}
