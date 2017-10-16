import QtQuick 2.5

import DICE.App 1.0
import DICE.App.Foam 1.0

Body {
    Card {
        title: qsTr("Mesh Quality Controls")

        spacing: 30

        Item {width:1; height:1}

        ValueField {
            label: "Maximum non-orthogonality allowed [°]"
            path: "foam:system/meshQualityDict maxNonOrtho"
            dataType: "int"
        }
        ValueField {
            label: "Max Internal Skewness allowed [°]"
            path: "foam:system/meshQualityDict maxInternalSkewness"
            dataType: "int"
        }
        ValueField {
            label: "Max Concaveness allowed [°]"
            path: "foam:system/meshQualityDict maxConcave"
            dataType: "int"
        }
        ValueField {
            label: "Minimum pyramid volume"
            path: "foam:system/meshQualityDict minVol"
        }
        ValueField {
            label: "Minimum quality of the tet"
            path: "foam:system/meshQualityDict minTetQuality"
        }
        ValueField {
            label: "minArea"
            path: "foam:system/meshQualityDict minArea"
        }
        ValueField {
            label: "minTwist"
            path: "foam:system/meshQualityDict minTwist"
        }
        ValueField {
            label: "Minimum normalised cell determinant"
            path: "foam:system/meshQualityDict minDeterminant"
        }
        ValueField {
            label: "minFaceWeight"
            path: "foam:system/meshQualityDict minFaceWeight"
        }
        ValueField {
            label: "minVolRatio"
            path: "foam:system/meshQualityDict minVolRatio"
        }
        ValueField {
            label: "minTriangleTwist"
            path: "foam:system/meshQualityDict minTriangleTwist"
        }
    }
}
