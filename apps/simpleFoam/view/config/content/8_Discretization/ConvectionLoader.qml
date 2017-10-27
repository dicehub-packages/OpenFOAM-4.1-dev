import QtQuick.Controls 1.4
import QtQuick 2.5
import QtQml.Models 2.2
import QtQuick.Layouts 1.3

import DICE.App 1.0
import DICE.Components 1.0

ConvectionSettings {
    path: {
        switch (modelData.modelData) {
            case 'Velocity':
                return "foam:system/fvSchemes divSchemes div(phi,U) %tuple"
            case 'k':
                return "foam:system/fvSchemes divSchemes div(phi,k) %tuple"
            case 'Epsilon':
                return "foam:system/fvSchemes divSchemes div(phi,epsilon) %tuple"
            case 'Omega':
                return "foam:system/fvSchemes divSchemes div(phi,omega) %tuple"
        }
    }
    grad: {
        switch (modelData.modelData) {
            case 'Velocity':
                return "grad(U)"
            case 'k':
                return "grad(k)"
            case 'Epsilon':
                return "grad(epsilon)"
            case 'Omega':
                return "grad(omega)"
        }
    }
    vector: modelData.modelData === 'Velocity'
}
