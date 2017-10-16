import DICE.App 1.0

Body {
    Card {
        title: "File output format"

        ValueField {
            label: "Write precision"
            dataType: "int"
            path: "foam:system/controlDict writePrecision"
        }
    }
}
