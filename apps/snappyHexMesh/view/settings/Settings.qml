import QtQuick 2.7

import DICE.Components 1.0

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

                    DiceSwitch {
                        id: useDocker
                        text: qsTr('Use OpenFOAM in Docker')
                        checked: settings.use_docker
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

                        SubheaderText {
                            text: "Docker command to start container with OpenFOAM"
                        }
                        DiceTextField {
                            width: parent.width
                            text: settings.docker_cmd
                            onTextChanged: settings.docker_cmd = text
                        }

                        SubheaderText {
                            text: "Docker command to start container with OpenFOAM and MPI"
                        }
                        DiceTextField {
                            width: parent.width
                            text: settings.docker_cmd_mpi
                            onTextChanged: settings.docker_cmd_mpi = text
                        }
                    }

                    Column {
                        width: parent.width
                        visible: !useDocker.checked
                        spacing: 20

                        SubheaderText {
                            text: "Path to $OpenFOAM/bin/foamExec"
                        }
                        DiceTextField {
                            width: parent.width
                            text: settings.foam_cmd
                            onTextChanged: settings.foam_cmd = text
                        }

                        SubheaderText {
                            text: "Path to mpirun"
                        }
                        DiceTextField {
                            width: parent.width
                            text: settings.foam_cmd_mpi
                            onTextChanged: settings.foam_cmd_mpi = text
                        }
                        SubheaderText {
                            text: "Paraview"
                        }
                        DiceTextField {
                            width: parent.width
                            text: settings.paraview_cmd
                            onTextChanged: settings.paraview_cmd = text
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
