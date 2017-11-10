import QtQuick 2.9

import DICE.App 1.0
import DICE.Components 1.0 as DC


Column {
    id: root

    property string grad

    width: parent.width
    spacing: 5

    DiceSwitch {
        id: useDefaultSchemeSwitch
        text: "Use default scheme"
        visible: grad !== "default"
        enabled: visible
        checked: useDefaultScheme
        onClicked: {
            useDefaultScheme = !useDefaultScheme
        }
    }

    ListView {
        id: interpolationSchemesList
        enabled: !useDefaultScheme
        visible: enabled
        model: ListModel {
            Component.onCompleted: {
                for (var i = 0; i < interpolationSchemesModel.length; i++) {
                    append(interpolationSchemesModel[i])
                }
                interpolationSchemesList.currentIndex = currentInterpolationSchemeListIndex
            }
        }
        delegate: InterpolationSchemeDelegate {

        }
        section.property: "sectionName"
        section.delegate: DC.HighlightBasicText {
            text: section
            type: "highlight"
            width: parent.width
            height: 25
        }
        width: parent.width
        height: childrenRect.height
        clip: true
        interactive: false
        onEnabledChanged: {
            if (currentIndex != currentInterpolationSchemeListIndex )
                currentIndex = currentInterpolationSchemeListIndex
        }
    }

    Item {
        width: 1
        height: 20
    }

    DiceInputField {
        width: parent.width
        visible: hasCoeff
        enabled: visible
        label: "Coefficient"
        text: !!coeff ? coeff : ""
        onTextChanged: {
            coeff = text
        }
        onEnabledChanged: {
            if (enabled)
                text = coeff
        }
    }

    DiceCheckBox {
        text: "Bounded"
        checked: isBounded
        enabled: !useDefaultScheme
        visible: enabled
        onClicked: {
            isBounded = !isBounded
        }
    }

    DiceCheckBox {
        text: "Improved"
        checked: improved
        enabled: improvementAllowed
        visible: enabled
        onClicked: {
            improved = !improved
        }
    }

    DC.HighlightBasicText {
        text: name + " " + schemeValue
        width: parent.width
        height: 50
        type: "highlight"
    }
}
