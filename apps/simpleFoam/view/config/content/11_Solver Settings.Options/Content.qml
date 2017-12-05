import DICE.App 1.0

Body {
    TabsCard3 {
        title: qsTr("Discretization")
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
                        'Omega'
                    ]
                case 'kEpsilon': [
                        'Pressure',
                        'Velocity',
                        'k',
                        'Epsilon'
                    ]
            }
        }
        delegateSource: "../../../../../../shared/qml/Solver/SolverLoader.qml"
        textRole: 'modelData'
    }
}
