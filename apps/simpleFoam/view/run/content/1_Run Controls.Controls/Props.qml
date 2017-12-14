import QtQuick 2.9

Loader {
    width: parent.width
    height: !!item ? item.height : 0
    source: {
        switch (modelData.modelData) {
        case "Run":
            return "Run.qml"
        case "Write":
            return "Write.qml"
        }
    }
}
