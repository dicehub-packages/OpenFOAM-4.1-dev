import QtQuick 2.5
import QtQuick.Controls 2.0

import DICE.App 1.0
import DICE.Components 1.0

Column {
    width: parent.width

    spacing: 5

    ValueConnector {
        id: gradScheme
        path: "foam:system/fvSchemes gradSchemes grad(T)"
    }

    ValueConnector {
        id: gradSchemeTuple
        path: "foam:system/fvSchemes gradSchemes grad(T) %tuple"
    }

    ValueConnector {
        id: snGradScheme
        path: "foam:system/fvSchemes snGradSchemes default"
    }

    ValueConnector {
        id: snGradSchemeTuple
        path: "foam:system/fvSchemes snGradSchemes default %tuple"
    }

    Subheader {
        text: "Gradient"
    }

    // ButtonGroup.group { id: gradientGroup }
    ButtonGroup { id: gradientGroup }

    RadioButton {
        id: gauss
        text: "Gauss"
        checked: !!gradSchemeTuple.value && gradSchemeTuple.value[0] == "Gauss"
        ButtonGroup.group: gradientGroup
        onClicked: {
            gradSchemeTuple.value =  ["Gauss", "linear"];
        }
    }

    DropDown2 {
        visible: gauss.checked
        path: visible ? "foam:system/fvSchemes gradSchemes grad(T) 1" : ""
        model: ["linear", "cubic"]
    }

    RadioButton {
        text: "Least Squares"
        ButtonGroup.group: gradientGroup
        checked: gradScheme.value == "leastSquares"
        onClicked: gradScheme.value = "leastSquares"
    }


    Subheader {
        text: "Surface Normal Gradient"
    }

    // ButtonGroup.group { id: snGradientGroup }
    ButtonGroup { id: snGradientGroup }

    RadioButton {
        text: "Corrected"
        ButtonGroup.group: snGradientGroup
        checked: snGradScheme.value == "corrected"
        onClicked: snGradScheme.value = "corrected"
    }

    RadioButton {
        text: "Uncorrected"
        ButtonGroup.group: snGradientGroup
        checked: snGradScheme.value == "uncorrected"
        onClicked: snGradScheme.value = "uncorrected"
    }
    
    RadioButton {
        id: limited
        text: "Limited"
        ButtonGroup.group: snGradientGroup
        checked: !!snGradSchemeTuple.value && snGradSchemeTuple.value[0] == "limited"
        onClicked: {
            snGradSchemeTuple.value = ["limited", "corrected", 0.5];
        }
    }

    ValueField {
        visible: limited.checked
        path: visible ? "foam:system/fvSchemes snGradSchemes default 2" : ""
    }

    RadioButton {
        text: "Orthogonal"
        ButtonGroup.group: snGradientGroup
        checked: snGradScheme.value == "orthogonal"
        onClicked: snGradScheme.value = "orthogonal"
    }
    
}
