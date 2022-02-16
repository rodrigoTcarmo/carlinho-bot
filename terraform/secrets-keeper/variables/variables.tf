variable "user" {
    type = string
    description = "*** Enter the secrets-keeper user name. Vide docs for more information: https://docs.cloud.intranet.pags/cofresegredos/primeiro-acesso/"
}

variable "user_password" {
    type = string
    sensitive = true
}

variable "operation" {
    type = string
    description = "*** The operation result for terraform execution"
    validation {
        condition = can(regex("^(?:register|grant-permission)$", var.operation))
        error_message = "The var operation must follow the regex pattern: ^(?:register|grant-permission)$."
    }
}

variable "project_team" {
    type = string
    description = "*** The reponsible team of this secrets-keeper instance" 
    validation {
        condition = can(regex("^[a-z0-9_]+$", var.project_team))
        error_message = "The var project_team must follow the regex pattern: ^[a-z0-9_]+$."
    }
}

variable "project_name" {
    type = string
    description = "*** The project name that will use the resource"
    validation {
        condition = can(regex("^[a-z0-9_]+$", var.project_name))
        error_message = "The var project_name must follow the regex pattern: ^[a-z0-9_]+$."
    }
}

variable "must_ignore_invalid_ssl_certificate" {
    default = true
}

variable "allow_range" {
    type = string
    description = "*** Allowed values: PagCloud | AWS"
    validation {
      condition = can(regex("^(?:PagCloud|AWS)$", var.allow_range))
      error_message = "The var allow_range must follow the regex pattern: ^(PagCloud|AWS)$."
    }
}

variable "environment" {
    type = string
    description = "*** Allowed values: Dev | QA | Prod"
    validation {
      condition = can(regex("^(?:Dev|QA|Prod)$", var.environment))
      error_message = "The var environment must follow the regex pattern: ^(?:Dev|QA|Prod)$."
    }
}

variable "domain" {
    type = string
    description = "*** Vide docs for more information: https://docs.cloud.intranet.pags/cofresegredos/cofre-de-segredos/"
}

variable "subdomain"{
    type = string
    description = "*** Vide docs for more information: https://docs.cloud.intranet.pags/cofresegredos/cofre-de-segredos/"
}

variable "topdomain" {
    type = string
    description = "*** Vide docs for more information: https://docs.cloud.intranet.pags/cofresegredos/cofre-de-segredos/"
}
