import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.3

import DICE.Components 1.0
// import DICE.Components 1.0 as DC

Item {
    id: root
    anchors.fill: parent

    Rectangle {
        id: background
        anchors.fill: parent
        anchors.margins: 5
        color: colors.secondary4BackgroundColor
        Frame {}

        ScrollView_DICE {
            id: scrollView
            anchors.fill: parent

            Column {
                width: scrollView.contentWidth

                spacing: 10

                Row {
                    anchors.left: parent.left
                    anchors.right: parent.right
                    spacing: 10

                    ToggleButton {
                        id: useDocker
                        width: parent.width/2
                        label: qsTr('Use OpenFOAM in Docker')
                        checked: settings.use_docker
                        uncheckedText: qsTr("no")
                        checkedText: qsTr("Yes")
                        onCheckedChanged: settings.use_docker = checked
                    }
                }

                Item {
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.margins: 10
                    height: childrenRect.height

                    Column {
                        width: parent.width
                        visible: useDocker.checked
                        spacing: 20

                        InputField {
                            label: "Docker command to start container with OpenFOAM"
                            Layout.fillWidth: true
                            text: settings.docker_cmd
                            onTextChanged: settings.docker_cmd = text
                        }

                        InputField {
                            label: "Docker command to start container with MPI"
                            Layout.fillWidth: true
                            text: settings.docker_cmd_mpi
                            onTextChanged: settings.docker_cmd_mpi = text
                        }
                    }

                    Column {
                        width: parent.width
                        visible: !useDocker.checked
                        spacing: 20

                        InputField {
                            label: "Path to $OpenFOAM/bin/foamExec"
                            Layout.fillWidth: true
                            text: settings.foam_cmd
                            onTextChanged: settings.foam_cmd = text
                        }

                        InputField {
                            label: "Path to mpirun"
                            Layout.fillWidth: true
                            text: settings.foam_cmd_mpi
                            onTextChanged: settings.foam_cmd_mpi = text
                        }

                    }
                }
            }  
        }
    }

    function listProperty(item){
        for(var p in item)
            console.log(item + "." + p + ": " + item[p]);
    }

    Component.onCompleted: listProperty(settings)

}
