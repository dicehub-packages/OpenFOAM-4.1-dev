import QtQuick 2.5
import QtQuick.Controls 2.2 as QQC

import DICE.App 1.0


Column {
    width: parent.width
    spacing: 5

    DiceValueConnector {
        id: gradScheme
        path: "foam:system/fvSchemes gradSchemes grad(T)"
    }

    DiceValueConnector {
        id: gradSchemeTuple
        path: "foam:system/fvSchemes gradSchemes grad(T) %tuple"
    }

    DiceValueConnector {
        id: snGradScheme
        path: "foam:system/fvSchemes snGradSchemes default"
    }

    DiceValueConnector {
        id: snGradSchemeTuple
        path: "foam:system/fvSchemes snGradSchemes default %tuple"
    }

    Subheader {
        text: "Gradient"
    }

    QQC.ButtonGroup { id: gradientGroup }

    DiceRadioButton {
        id: gauss
        text: "Gauss"
        checked: !!gradSchemeTuple.value && gradSchemeTuple.value[0] === "Gauss"
        QQC.ButtonGroup.group: gradientGroup
        onClicked: {
            gradSchemeTuple.value =  ["Gauss", "linear"];
        }
    }

    DiceInlineComboBox {
        visible: gauss.checked
        path: visible ? "foam:system/fvSchemes gradSchemes grad(T) 1" : ""
        model: ["linear", "cubic"]
    }

    DiceRadioButton {
        text: "Least Squares"
        QQC.ButtonGroup.group: gradientGroup
        checked: gradScheme.value === "leastSquares"
        onClicked: gradScheme.value = "leastSquares"
    }


    Subheader {
        text: "Surface Normal Gradient"
    }

    QQC.ButtonGroup { id: snGradientGroup }

    DiceRadioButton {
        text: "Corrected"
        QQC.ButtonGroup.group: snGradientGroup
        checked: snGradScheme.value === "corrected"
        onClicked: snGradScheme.value = "corrected"
    }

    DiceRadioButton {
        text: "Uncorrected"
        QQC.ButtonGroup.group: snGradientGroup
        checked: snGradScheme.value === "uncorrected"
        onClicked: snGradScheme.value = "uncorrected"
    }
    
    DiceRadioButton {
        id: limited
        text: "Limited"
        QQC.ButtonGroup.group: snGradientGroup
        checked: !!snGradSchemeTuple.value && snGradSchemeTuple.value[0] === "limited"
        onClicked: {
            snGradSchemeTuple.value = ["limited", "corrected", 0.5];
        }
    }

    DiceValueField {
        visible: limited.checked
        path: visible ? "foam:system/fvSchemes snGradSchemes default 2" : ""
    }

    DiceRadioButton {
        text: "Orthogonal"
        QQC.ButtonGroup.group: snGradientGroup
        checked: snGradScheme.value === "orthogonal"
        onClicked: snGradScheme.value = "orthogonal"
    }
    
}
