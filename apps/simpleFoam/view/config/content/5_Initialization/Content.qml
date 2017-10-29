import QtQuick 2.4
import QtQuick.Layouts 1.3
import QtQuick.Controls 1.4

import DICE.App 1.0
import DICE.Components 1.0

Body {
    TabsCard3 {
        title: qsTr("Discretization")
        model:  {
            switch (app.turbulenceModel) {
                case 'laminar':
                    return [
                        'Pressure',
                        'Velocity'
                    ]
                case 'kOmegaSST':
                    return [
                        'Pressure',
                        'Velocity',
                        'k',
                        'Omega',
                        'nut'
                    ]
                case 'kEpsilon': [
                        'Pressure',
                        'Velocity',
                        'k',
                        'Epsilon',
                        'nut'
                    ]
            }
        }
        delegateSource: "Initialization.qml"
        textRole: 'modelData'
    }
}
