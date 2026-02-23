pipeline {
    agent { label 'docker-agent' }

    environment {
        IMAGE_NAME = "anu2706/travel_web_app"
        TAG = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
        PREPROD_USER = "ubuntu"
        PREPROD_HOST = "13.219.143.91"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$TAG .'
            }
        }
    
    stage('Run Tests (inside Docker)') {
        steps {
            sh 'docker run --rm $IMAGE_NAME:$TAG pytest'
        }
    }

        stage('Push Image to DockerHub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                      echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                      docker push $IMAGE_NAME:$TAG
                    '''
                }
            }
        }

        stage('Deploy to PreProd') {
            steps {
                sshagent(['preprod-key']) {
                    sh """
                      ssh -o StrictHostKeyChecking=no $PREPROD_USER@$PREPROD_HOST "
                      docker pull $IMAGE_NAME:$TAG &&
                      docker stop travel || true &&
                      docker rm travel || true &&
                      docker run -d -p 5000:5000 --name travel $IMAGE_NAME:$TAG
                      "
                    """
                }
            }
        }
    }

    post {
        success {
            echo "✅ Travel Flask App deployed successfully to Pre-Production"
        }
        failure {
            echo "❌ Pipeline failed. Check logs."
        }
    }
}
