import DICE.App 1.0


GradientsSettings {
    path: {
        switch (modelData.modelData) {
            case 'Default':
                return "foam:system/fvSchemes gradSchemes"
            case 'Velocity':
                return "foam:system/fvSchemes gradSchemes"
            case 'Pressure':
                return "foam:system/fvSchemes gradSchemes"
            case 'k':
                return "foam:system/fvSchemes gradSchemes"
            case 'Epsilon':
                return "foam:system/fvSchemes gradSchemes"
            case 'Omega':
                return "foam:system/fvSchemes gradSchemes"
        }
    }

    grad: {
        switch (modelData.modelData) {
            case 'Default':
                return "default"
            case 'Velocity':
                return "grad(U)"
            case 'Pressure':
                return "grad(p)"
            case 'k':
                return "grad(k)"
            case 'Epsilon':
                return "grad(epsilon)"
            case 'Omega':
                return "grad(omega)"
        }
    }
}
