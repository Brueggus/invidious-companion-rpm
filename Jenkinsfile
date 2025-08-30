pipeline {
  agent none
  options {
    timestamps()
  }
  stages {
    stage('build') {
      parallel {
        stage('fedora-41') {
          agent { label 'fedora-41-rpm-isolated' }
          steps {
            sh '''
              sudo dnf copr enable --assumeyes pgdev/deno
              rpmtool build invidious-companion.spec
              mkdir --parents "${WORKSPACE}/artifacts"
              cp --verbose ${HOME}/rpmbuild/SRPMS/*.rpm "${WORKSPACE}/artifacts/"
              cp --verbose ${HOME}/rpmbuild/RPMS/**/*.rpm "${WORKSPACE}/artifacts/"
            '''
            archiveArtifacts artifacts: 'artifacts/**/*', fingerprint: true, onlyIfSuccessful: true
          }
        }
        stage('fedora-42') {
          agent { label 'fedora-42-rpm-isolated' }
          steps {
            sh '''
              sudo dnf copr enable --assumeyes pgdev/deno
              rpmtool build invidious-companion.spec
              mkdir --parents "${WORKSPACE}/artifacts"
              cp --verbose ${HOME}/rpmbuild/SRPMS/*.rpm "${WORKSPACE}/artifacts/"
              cp --verbose ${HOME}/rpmbuild/RPMS/**/*.rpm "${WORKSPACE}/artifacts/"
            '''
            archiveArtifacts artifacts: 'artifacts/**/*', fingerprint: true, onlyIfSuccessful: true
          }
        }
      }
    }
    stage('copr') {
      agent { label 'fedora-42-rpm' }
      when {
        expression { env.GIT_BRANCH == 'origin/master' }
      }
      steps {
        withCredentials([file(credentialsId: 'pgdev-copr-api', variable: '__COPR_API_CONFIG')]) {
          sh '''
            copr --config "$__COPR_API_CONFIG" build-package --nowait --background --name invidious-companion pgdev/invidious
          '''
        }
      }
    }
  }
  post {
    failure {
      emailext(
        to: '$DEFAULT_RECIPIENTS',
        subject: '$DEFAULT_SUBJECT',
        body: '$DEFAULT_CONTENT',
      )
    }
    fixed {
      emailext(
        to: '$DEFAULT_RECIPIENTS',
        subject: '$DEFAULT_SUBJECT',
        body: '$DEFAULT_CONTENT',
      )
    }
  }
}
