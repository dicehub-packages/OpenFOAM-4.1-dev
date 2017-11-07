import QtQuick 2.9
import QtQuick.Layouts 1.3

import DICE.App 1.0

Body {
    Card {
        title: qsTr('Decomposition')
        spacing: 30

        DiceSwitch {
            text: qsTr("Activate Parallel Run")
            path: "config:parallelRun"
        }

        Subheader{ text: qsTr("Decomposition Options") }

        DiceValueField {
            label: qsTr("Number of Subdomains")
            path: "foam:system/decomposeParDict numberOfSubdomains"
            dataType: "int"
        }

        Row {
        	width: parent.width
            Caption {
                text: qsTr("Method")
                width: parent.width/2
            }
            DiceComboBox {
	            id: methodDropDown
                model: [ "hierarchical", "simple", "scotch" ]
	            currentIndex: -1
                width: parent.width/2
                DiceValueConnector {
	            	id: methodValue
	            	path: "foam:system/decomposeParDict method"
	            	onReady: {
            			methodDropDown.currentIndex = methodDropDown.find(value)
            			value = Qt.binding(function(){return methodDropDown.currentText})
	            	}
	            }
        	}
        }

        Subheader {
            text: qsTr("Coefficients")
            visible: methodDropDown.currentText !== "scotch"
        }

        DiceVectorField {
            xLabel: "n_x"
            yLabel: "n_y"
            zLabel: "n_z"
            path: "foam:system/decomposeParDict " + methodDropDown.currentText + "Coeffs n"
        	dataType: 'int'
            visible: methodDropDown.currentText !== "scotch"
        }

        DiceValueField {
            label: qsTr("Delta")
            path: "foam:system/decomposeParDict " + methodDropDown.currentText + "Coeffs delta"
            visible: methodDropDown.currentText !== "scotch"
        }

        Row {
        	width: parent.width
        	visible: methodDropDown.currentText === "hierarchical"
            Caption {
                text: qsTr("Order")
                width: parent.width/2
            }
            DiceComboBox {
	            id: orderDropDown
	            model: ["xyz", "yxz", "yzx", "xzy", "zxy", "zyx"]
	            currentIndex: -1
                width: parent.width/2
                DiceValueConnector {
	            	id: methodValue2
	            	path: "foam:system/decomposeParDict hierarchicalCoeffs order"
	            	onReady: {
            			orderDropDown.currentIndex = orderDropDown.find(value)
            			value = Qt.binding(function(){return orderDropDown.currentText})
	            	}
	            }
        	}
        }
    }
}
