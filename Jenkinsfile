pipeline {
    agent any

    environment {
        PROJECT_NAME = "support-ticket"
    }

    stages {

        stage('🔁 Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Affichage de fichiers') {
            steps {
                sh 'ls -la'
            }
        }

        stage('💬 Hello World') {
            steps {
                echo "🎉 Jenkins est connecté au repo !"
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline terminé avec succès"
        }
        failure {
            echo "❌ Une erreur est survenue pendant le pipeline"
        }
    }
}
