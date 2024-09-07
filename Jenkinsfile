pipeline {
    agent any
    environment {
        // Define environment variables for Telegram bot
        TELEGRAM_BOT_TOKEN = '6790816236:AAFmBx0K4blTxcBHRlSAtVBRDWOacF9BQ3U'
        TELEGRAM_CHAT_ID = '1017399433'
        PROJECT_NAME = "${env.JOB_NAME}"
        PIPELINE_LINK = "${env.BUILD_URL}"  // Jenkins pipeline URL
        TRIGGERED_USER = "${env.CHANGE_AUTHOR}"  // User triggering the pipeline
        TXT_FILE = 'test.txt'  // The text file used to simulate success/failure
    }
    
    stages {
        stage('Notify Start') {
            steps {
                script {
                    sendTelegramMessage("🔔 *Pipeline Triggered*\n*Project:* ${env.PROJECT_NAME}\n*Pipeline Link:* ${env.PIPELINE_LINK}\n*Triggered by:* ${env.TRIGGERED_USER}")
                }
            }
        }

        stage('Build Image') {
            steps {
                script {
                    def buildSuccess = checkBuildSuccess()
                    if (!buildSuccess) {
                        error "Build failed due to the content of the text file."
                    } else {
                        sendTelegramMessage("✅ *Build Stage Successful*\n*Project:* ${env.PROJECT_NAME}\n*Pipeline Link:* ${env.PIPELINE_LINK}\n*Triggered by:* ${env.TRIGGERED_USER}")
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    def deploySuccess = checkDeploySuccess()
                    if (!deploySuccess) {
                        error "Deploy failed due to the content of the text file."
                    } else {
                        sendTelegramMessage("🚀 *Deploy Stage Successful*\n*Project:* ${env.PROJECT_NAME}\n*Pipeline Link:* ${env.PIPELINE_LINK}\n*Triggered by:* ${env.TRIGGERED_USER}")
                    }
                }
            }
        }
    }

    post {
        success {
            script {
                sendTelegramMessage("🎉 *Pipeline Completed Successfully*\n*Project:* ${env.PROJECT_NAME}\n*Pipeline Link:* ${env.PIPELINE_LINK}\n*Triggered by:* ${env.TRIGGERED_USER}")
            }
        }
        failure {
            script {
                sendTelegramMessage("❌ *Pipeline Failed*\n*Project:* ${env.PROJECT_NAME}\n*Pipeline Link:* ${env.PIPELINE_LINK}\n*Triggered by:* ${env.TRIGGERED_USER}")
            }
        }
    }
}

def sendTelegramMessage(message) {
    sh """
    curl -s -X POST https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage \
    -d chat_id=${env.TELEGRAM_CHAT_ID} \
    -d text="${message}" \
    -d parse_mode=Markdown
    """
}

def checkBuildSuccess() {
    // Read the first line of the file for build status
    def lines = readFile(env.TXT_FILE).split('\n')
    return lines[0].trim() == 'build_success'
}

def checkDeploySuccess() {
    // Read the second line of the file for deploy status
    def lines = readFile(env.TXT_FILE).split('\n')
    return lines.length > 1 && lines[1].trim() == 'deploy_success'
}
