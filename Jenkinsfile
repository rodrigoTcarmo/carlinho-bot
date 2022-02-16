#!groovy

import br.com.uol.ps.pipelineutils.SlackAPI
import br.com.uol.ps.pipelineutils.ProjectRelease
import br.com.uol.ps.pipelineutils.KubernetesHelper

def slackAPI = new SlackAPI(this)

def branchSelected = "${env.BRANCH_SELECTED}"

node("python-3.8"){

    def project_name = ""
    def app_port = 80
    def k8s_namespace = ""
    def slack_channel = ""
    def branch = ""
    def tag_version = ""
    def vault_role_id = ""
    def vault_secret_id = ""
    def vault_namespace = ""
    def vault_environments = ["qa": new Vault("", "")]

    if (branchSelected.contains("master")){
        println "Project is not ready to deploy to production!"
        println "Setting QA environment - just to avoid disaster ;)"
        environment = "qa"
        branch = "develop"

    } else{
        environment = "qa"
        branch = "develop"
    }

    vault_role_id = vault_environments.get(environment).role_id
    vault_secret_id = vault_environments.get(environment).role_id

    deleteDir()

    stage(name: "Git checkout"){
        checkout([$class: 'GitSCM',
            branches: [[name: branchSelected]],
            doGenerateSubmoduleConfigurations: false,
            extensions                       : [],
            submoduleCfg                     : [],
            userRemoteConfigs                : [[url: ""]]
        ])

        branchCheckout = scm.branches[0].name
        println "Branch: ${env.BRANCH_SELECTED}"

    }

    stage(name: "Release Version"){
        tag_version = version_manager(branch)
        echo "${tag_version}"
    }

    stage(name: "Prepare deploy"){
        sh "echo Preparing deploy..."
        def project_group = "investments-docker-${environment}"
        docker_build(tag_version, project_group, project_name)
        prepare_deploy(project_name, project_group, k8s_namespace, environment, tag_version, vault_role_id, vault_secret_id, vault_namespace)
    }

    stage(name: "deployQA") {
        sh "echo Start deploy on K8S env: ${environment}"
        def kubernetesHelper = new KubernetesHelper(this)
        kubernetesHelper.deployTo(environment)
    }

}

def version_manager(branch) {
    def version = ""
    release_engine = new ProjectRelease(this, branch)
    if (branch == "develop") {
        echo "Setting up new version..."
//         version = sh(script: "git describe --tags --abbrev=0 | awk -F. \'{print substr($1,2)"."$2"."$3+1}\''", returnStdout: true)
        version = sh(script: "python3 deploy_files/versions.py", returnStdout: true)
        echo "Versio: ${version}"
    }
    return version

}

def docker_build(tag_version, project_group, project_name) {
    echo "Starting docker build..."
    app = docker.build("${project_group}/${project_name}", ".")
    docker.withRegistry("", "") {
        app.push(tag_version)
    }
}

def prepare_deploy(project_name, project_group, k8s_namespace, environment, tag_version, vault_role_id, vault_secret_id, vault_namespace) {
    dc = ['gt', 'tb']

    for (int i = 0; i < dc.size(); i++) {
        def text = readFile file: "deploy.yaml"
        def new_file = text.replaceAll("project_name", project_name)
                           .replaceAll("project_group", project_group)
                           .replaceAll("tag_version", tag_version)
                           .replaceAll("vault_role_id", vault_role_id)
                           .replaceAll("vault_secret_id", vault_secret_id)
                           .replaceAll("vault_namespace", vault_namespace)

        writeFile file: "deploy/${environment}/${dc[i]}.yaml", text: new_file
    }
}

class Vault {
    String role_id
    String secret_id

    Vault(role_id, secret_id) {
        this.role_id = role_id
        this.secret_id = secret_id
    }
}
