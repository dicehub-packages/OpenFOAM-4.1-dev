import QtQuick 2.9

import DICE.App 1.0

Body {
    Card {
        title: qsTr("Mesh Quality Controls")

        spacing: 30

        DiceValueField {
            label: "Maximum non-orthogonality allowed [°]"
            path: "foam:system/meshQualityDict maxNonOrtho"
            dataType: "int"
        }
        DiceValueField {
            label: "Maximum Internal Skewness allowed [°]"
            path: "foam:system/meshQualityDict maxInternalSkewness"
            dataType: "int"
        }
        DiceValueField {
            label: "Maximum Concaveness allowed [°]"
            path: "foam:system/meshQualityDict maxConcave"
            dataType: "int"
        }
        DiceValueField {
            label: "Minimum pyramid volume"
            path: "foam:system/meshQualityDict minVol"
        }
        DiceValueField {
            label: "Minimum quality of the tet"
            path: "foam:system/meshQualityDict minTetQuality"
        }
        DiceValueField {
            label: "Minimum Area"
            path: "foam:system/meshQualityDict minArea"
        }
        DiceValueField {
            label: "Minimum Twist"
            path: "foam:system/meshQualityDict minTwist"
        }
        DiceValueField {
            label: "Minimum normalised cell determinant"
            path: "foam:system/meshQualityDict minDeterminant"
        }
        DiceValueField {
            label: "Minimal FaceWeight"
            path: "foam:system/meshQualityDict minFaceWeight"
        }
        DiceValueField {
            label: "Minimum VolRatio"
            path: "foam:system/meshQualityDict minVolRatio"
        }
        DiceValueField {
            label: "Minimum TriangleTwist"
            path: "foam:system/meshQualityDict minTriangleTwist"
        }
    }
}
