import QtQuick 2.9

import DICE.App 1.0


Column {
    id: root

    property alias path: divScheme.path
    property bool vector: false
    property string grad
    width: parent.width

    spacing: 5

    DiceValueConnector {
        id: divScheme
    }

    function cleanValue() {
        return divScheme.value.filter(function(item) { 
            return ([
                'bounded', 
                'Gauss',
                'skewCorrected'
                ]).indexOf(item) >= 0;
        });
    }

    function setValue(value) {
        divScheme.value = value;
    }

    DiceRadioButton {
        text: "Upwind"
        checked: divScheme.isValid && divScheme.value.indexOf('upwind') >= 0
        onClicked: {
            var value = root.cleanValue();
            value.splice(value.length, 0, "upwind");
            root.setValue(value);
        }
    }

    DiceRadioButton {
        text: "Linear Upwind"
        checked: divScheme.isValid && (divScheme.value.indexOf('linearUpwind') >= 0 ||
            divScheme.value.indexOf('linearUpwindV') >= 0)
        onClicked: {
            var value = root.cleanValue();
            if (vecSpec.checked)
                value.splice(value.length, 0, "linearUpwindV");
            else
                value.splice(value.length, 0, "linearUpwind");
            value.splice(value.length, 0, root.grad);
            root.setValue(value);
        }
    }

    DiceRadioButton {
        text: "Linear"
        checked: divScheme.isValid && (divScheme.value.indexOf('linear') >= 0)
        onClicked: {
            var value = root.cleanValue();
            value.splice(value.length, 0, "linear");
            root.setValue(value);
        }
    }

    DiceRadioButton {
        id: limLinear
        text: "Limited Linear"
        checked: divScheme.isValid && (divScheme.value.indexOf('limitedLinear') >= 0 ||
            divScheme.value.indexOf('limitedLinearV') >= 0)
        onClicked: {
            var value = root.cleanValue();
            if (vecSpec.checked)
                value.splice(value.length, 0, "limitedLinearV");
            else
                value.splice(value.length, 0, "limitedLinear");
            value.splice(value.length, 0, 1);
            root.setValue(value);
        }
    }

    DiceValueField {
        visible: limLinear.checked
        path: (divScheme.isValid && (divScheme.value.indexOf('limitedLinear') >= 0 ||
            divScheme.value.indexOf('limitedLinearV') >= 0)) ? (divScheme.path + " -1") : ""
        dataType: "int"
    }

    DiceCheckBox {
        id: vecSpec
        text: "Vector Specific"
        enabled: root.vector && (checked || (divScheme.isValid && (divScheme.value.indexOf('linearUpwind') >= 0 ||
            divScheme.value.indexOf('limitedLinear') >= 0)))
        checked: divScheme.isValid && (divScheme.value.indexOf('linearUpwindV') >= 0 ||
            divScheme.value.indexOf('limitedLinearV') >= 0)

        onClicked: {
            if (divScheme.value.indexOf('linearUpwind')) {
                value = divScheme.value.slice()
                value[divScheme.value.indexOf('linearUpwind')] = "linearUpwindV"
            } else if (divScheme.value.indexOf('limitedLinear')) {
                value = divScheme.value.slice()
                value[divScheme.value.indexOf('limitedLinear')] = "limitedLinearV"
            }else if (divScheme.value.indexOf('linearUpwindV')) {
                value = divScheme.value.slice()
                value[divScheme.value.indexOf('linearUpwindV')] = "linearUpwind"
            } else if (divScheme.value.indexOf('limitedLinearV')) {
                value = divScheme.value.slice()
                value[divScheme.value.indexOf('limitedLinearV')] = "limitedLinear"
            }
            root.setValue(value)
        }
    }


    DiceCheckBox {
        text: "Bounded"
        checked: divScheme.isValid && divScheme.value.indexOf('bounded') >= 0
        onClicked: {
            var value;
            if (divScheme.value.indexOf('bounded') >= 0) {
                value = divScheme.value.slice()
                var index = divScheme.value.indexOf('bounded')
                value.splice(index, 1)
            } else {
                value = divScheme.value.slice()
                var index = divScheme.value.indexOf('Gauss')
                value.splice(index-1, 0, "bounded");
            }
            root.setValue(value)
        }
    }

    DiceCheckBox {
        text: "Skew Corrected"
        checked: divScheme.isValid && divScheme.value.indexOf('skewCorrected') >= 0
        onClicked: {
            var value;
            if (divScheme.value.indexOf('skewCorrected') >= 0) {
                value = divScheme.value.slice()
                var index = divScheme.value.indexOf('skewCorrected')
                value.splice(index, 1)
            } else {
                value = divScheme.value.slice()
                var index = divScheme.value.indexOf('Gauss')
                value.splice(index+1, 0, "skewCorrected");
            }
            root.setValue(value)
        }
    }

}
