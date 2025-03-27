pipeline {
    agent any

    environment {
        PROJECT_NAME = "support-ticket"
        DOCKER_IMAGE = "support-ticket-api"
    }

    stages {

        stage('🔁 Checkout') {
            steps {
                checkout scm
            }
        }

        stage('🐍 Setup Python') {
            steps {
                sh 'python -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('🧪 Run Tests') {
            steps {
                sh '. venv/bin/activate && pytest || echo "⚠️ Tests non bloquants"'
            }
        }

        stage('🐳 Build Docker Image') {
            steps {
                sh 'docker-compose build'
            }
        }

        stage('🚀 Deploy with Docker Compose') {
            steps {
                sh 'docker-compose down || true'
                sh 'docker-compose up -d'
            }
        }

    }

    post {
        success {
            echo "🎉 Déploiement réussi du backend !"
        }
        failure {
            echo "❌ Une erreur est survenue pendant le pipeline."
        }
    }
}
