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

        stage('📦 Docker Compose Build') {
            steps {
                sh 'docker-compose build'
            }
        }

        stage('🚀 Docker Compose Up') {
            steps {
                sh 'docker-compose down || true'
                sh 'docker-compose up -d'
            }
        }
    }

    post {
        success {
            echo "✅ Déploiement réussi via CI/CD 🎉"
        }
        failure {
            echo "❌ Une erreur est survenue pendant le pipeline."
        }
    }
}
