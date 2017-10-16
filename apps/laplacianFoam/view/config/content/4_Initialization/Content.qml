import QtQuick 2.4

import DICE.App 1.0
import DICE.App.Foam 1.0

Body {
    Card {
        title: "Temperature [K]"
        ValueField {
            path: "foam:0/T internalField %field"
        }
    }
}