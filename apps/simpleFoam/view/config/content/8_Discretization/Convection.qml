
import QtQuick 2.4
import QtQuick.Layouts 1.3
import QtQuick.Controls 1.4

import DICE.App 1.0
import DICE.Components 1.0

TabsCard3 {
    model: {
        switch (app.turbulenceModel) {
            case 'none':
                return [
                    'Velocity'
                ]
            case 'kOmegaSST':
                return [
                    'Velocity',
                    'k',
                    'Omega'
                ]
            case 'kEpsilon': [
                    'Velocity',
                    'k',
                    'Epsilon'
                ]
        }
    }
    delegateSource: "ConvectionLoader.qml"
    textRole: 'modelData'
}