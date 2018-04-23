#!groovy

def tryStep(String message, Closure block, Closure tearDown = null) {
    try {
        block();
    }
    catch (Throwable t) {
        slackSend message: "${env.JOB_NAME}: ${message} failure ${env.BUILD_URL}", channel: '#junk-kanaal', color: 'danger'

        throw t;
    }
    finally {
        if (tearDown) {
            tearDown();
        }
    }
}


node {

    stage("Checkout") {
        checkout scm
    }

    stage('Test') {
        tryStep "test", {
            sh "api/deploy/test/test.sh &&" +
               "scrape_api/deploy/test/test.sh"
        }
    }

    stage("Build dockers") {
        tryStep "build", {
            def importer = docker.build("build.datapunt.amsterdam.nl:5000/afvalcontainers_importer:${env.BUILD_NUMBER}", "scrape_api")
                importer.push()
                importer.push("acceptance")

            def api = docker.build("build.datapunt.amsterdam.nl:5000/afvalcontainers:${env.BUILD_NUMBER}", "api")
                api.push()
                api.push("acceptance")
        }
    }
}

String BRANCH = "${env.BRANCH_NAME}"

if (BRANCH == "master") {

    node {
        stage('Push acceptance image') {
            tryStep "image tagging", {
                def image = docker.image("build.datapunt.amsterdam.nl:5000/afvalcontainers:${env.BUILD_NUMBER}")
                image.pull()
                image.push("acceptance")
            }
        }
    }

    node {
        stage("Deploy to ACC") {
            tryStep "deployment", {
                build job: 'Subtask_Openstack_Playbook',
                parameters: [
                    [$class: 'StringParameterValue', name: 'INVENTORY', value: 'acceptance'],
                    [$class: 'StringParameterValue', name: 'PLAYBOOK', value: 'deploy-afvalcontainers.yml'],
                ]
            }
        }
    }

    stage('Waiting for approval') {
        slackSend channel: '#junk-kanaal', color: 'warning', message: 'Afval Container API Waiting for Production Release - please confirm'
        input "Deploy to Production?"
    }

    node {
        stage('Push production image') {
            tryStep "image tagging", {
                def api = docker.image("build.datapunt.amsterdam.nl:5000/afvalcontainers:${env.BUILD_NUMBER}")
                def importer = docker.image("build.datapunt.amsterdam.nl:5000/afvalcontainers_importer:${env.BUILD_NUMBER}")

                importer.push("production")
                importer.push("latest")

                api.push("production")
                api.push("latest")
            }
        }
    }

    node {
        stage("Deploy") {
            tryStep "deployment", {
                build job: 'Subtask_Openstack_Playbook',
                parameters: [
                        [$class: 'StringParameterValue', name: 'INVENTORY', value: 'production'],
                        [$class: 'StringParameterValue', name: 'PLAYBOOK', value: 'deploy-afvalcontainers.yml'],
                ]
            }
        }
    }
}
