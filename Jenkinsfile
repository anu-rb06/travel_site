pipeline {
    agent { label 'docker-agent' }

    environment {
        IMAGE_NAME = "anu2706/travel_web_app"
        TAG = "latest"
        PREPROD_USER = "ubuntu"
        PREPROD_HOST = "13.219.143.91"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git 'https://github.com/anu-rb06/travel_site.git'
            }
        }

        stage('Install Dependencies') {
            steps {
              sh '''
                python3 --version

                # Create virtual environment only if it does not exist
                if [ ! -d "travel_env" ]; then
                    echo "🆕 Creating virtual environment: travel_env"
                    python3 -m venv travel_env
                else
                    echo "♻️ Using existing virtual environment: travel_env"
                fi

                # Activate virtual environment
                . travel_env/bin/activate
    
                # Upgrade pip inside virtual environment
                pip install --upgrade pip

                # Install app dependencies
                pip install -r requirements.txt

                # Verify
                python --version
                pip list
                '''

            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                . travel_env/bin/activate
                pytest
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$TAG .'
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
