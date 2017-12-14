import DICE.App 1.0

Body {
    TabsCard3 {
        title: qsTr("Initialize")
        model:  {
            switch (app.turbulence.model) {
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
