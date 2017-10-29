import DICE.App 1.0

TabsCard3 {
    model: {
        switch (app.turbulenceModel) {
            case 'laminar':
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
