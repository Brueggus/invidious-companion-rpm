pipeline {
  agent none
  options {
    timestamps()
  }
  stages {
    stage('build') {
      parallel {
        stage('fedora-41-x86_64') {
          agent {
            node {
              label 'fedora-41-rpm-isolated'
              customWorkspace "${env.JOB_NAME}/${env.BUILD_ID}"
            }
          }
          steps {
            sh '''
              sudo dnf copr enable --assumeyes pgdev/deno
              rpmtool build invidious-companion.spec
              mkdir --parents "${WORKSPACE}/artifacts/f41"
              mv "${HOME}/rpmbuild/SRPMS" "${WORKSPACE}/artifacts/f41/"
              mv "${HOME}/rpmbuild/RPMS" "${WORKSPACE}/artifacts/f41/"
            '''
            stash includes: 'artifacts/f41/**/*', name: 'f41-x86_64'
          }
        }
        stage('fedora-42-x86_64') {
          agent {
            node {
              label 'fedora-42-rpm-isolated'
              customWorkspace "${env.JOB_NAME}/${env.BUILD_ID}"
            }
          }
          steps {
            sh '''
              sudo dnf copr enable --assumeyes pgdev/deno
              rpmtool build invidious-companion.spec
              mkdir --parents "${WORKSPACE}/artifacts/f42"
              mv "${HOME}/rpmbuild/SRPMS" "${WORKSPACE}/artifacts/f42/"
              mv "${HOME}/rpmbuild/RPMS" "${WORKSPACE}/artifacts/f42/"
            '''
            stash includes: 'artifacts/f42/**/*', name: 'f42-x86_64'
          }
        }
      }
    }
    stage('publish') {
      agent {
        node {
          label 'fedora-42'
          customWorkspace "${env.JOB_NAME}/${env.BUILD_ID}"
        }
      }
      steps {
        unstash 'f41-x86_64'
        unstash 'f42-x86_64'
        archiveArtifacts artifacts: 'artifacts/**/*', fingerprint: true, onlyIfSuccessful: true
      }
    }
    stage('copr') {
      agent {
        node {
          label 'fedora-42-rpm'
          customWorkspace "${env.JOB_NAME}/${env.BUILD_ID}"
        }
      }
      when {
        allOf {
          expression { params.COPR_BUILD == true }
          expression { env.GIT_BRANCH == 'origin/master' }
        }
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
