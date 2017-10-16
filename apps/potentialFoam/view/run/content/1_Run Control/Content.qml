import QtQuick 2.4
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.2

import DICE.App 1.0

Item {
    id: root
    anchors.fill: parent
    SplitView {
		anchors.fill: parent
    	Rectangle {
    		width: 200
    		height: parent.height
    		color: 'red'
    	}
    	Rectangle {
    		id: fig
            color: 'blue'
    		height: parent.height
    		Component.onCompleted: {
                app.plot.parent = this;
                app.plot.anchors.fill = this;
            }
    	}
    }
}
