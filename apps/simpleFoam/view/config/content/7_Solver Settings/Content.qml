import QtQuick 2.4
import QtQuick.Layouts 1.3
//import QtQuick.Controls 1.4

import DICE.App 1.0
//import DICE.Components 1.0

Body {
    TabsCard3 {
        title: qsTr("Discretization")
        model:  {
            switch (app.turbulenceModel) {
                case 'none':
                    return [
                        'p - Pressure',
                        'U - Velocity'
                    ]
                case 'kOmegaSST':
                    return [
                        'p - Pressure',
                        'U - Velocity',
                        'k',
                        'Omega'
                    ]
                case 'kEpsilon': [
                        'p - Pressure',
                        'U - Velocity',
                        'k',
                        'Epsilon'
                    ]
            }
        }
        delegateSource: "../../../../../../shared/qml/Solver/SolverLoader.qml"
        textRole: 'modelData'
    }
}
