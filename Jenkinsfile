pipeline {
    agent any
    environment {
        PATH = "/usr/local/nginx/sbin:/home/lee/Downloads/node-v10.16.0-linux-x64/bin:/home/lee/Downloads/yarn-v1.21.1/bin:${env.PATH}"
    }
    stages {
        stage('Build') {
            steps {
                sh "docker build . -t pythoner/agentmanager:latest"
                sh "docker push pythoner/agentmanager:latest"
               }
            }
        stage('deploy') {
            steps {
                sh 'kubectl apply -f k8s-deployment.yaml -n isddc'
                 }
             }
      }
}

