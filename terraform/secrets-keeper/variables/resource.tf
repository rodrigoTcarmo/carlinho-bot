locals {
    /*" Vide docs for more information: 
        https://docs.cloud.intranet.pags/documentacao-api/cofre-de-segredos/criando-via-api/
    "*/
    domain_vmware_vra_tokens = {
        register = {
            Dev  = "017cd276-20d5-441d-9826-a58ea4640bcb"
            QA   = "0c2a1e6a-440b-401c-9a22-49997901c680"
            Prod = "0c2a1e6a-440b-401c-9a22-49997901c680"
        }
        grant-permission = {
            Dev  = "8c432471-c91b-43d0-832c-527cb9016510"
            QA   = "51a50e22-dac8-47f7-8a1e-c57c471deb5c"
            Prod = "51a50e22-dac8-47f7-8a1e-c57c471deb5c"
        }
    }
    domain_operation = {
        register         = "Vault_-_Processo_Cofre_de_Segredos_1"
        grant-permission = "Vault_-_Processo_para_atualizar_os_Segredos_do_Cofre_1"
    }
    domain_operation_description = {
        register         = "Creating a new instance of secrets-keeper"
        grant-permission = "Grant user ${var.user} write permission for a 24h period in the secrets-keeper instance"
    }
    domain_lease_days = {
        register         = "0"
        grant-permission = "1"
    }
}

locals {
    resource_name             = "team-${var.project_team}-project-${var.project_name}-${lower(var.environment)}"
    resource_vmware_vra_token = local.domain_vmware_vra_tokens[var.operation][var.environment]
    resource_operation        = local.domain_operation[var.operation]
    resource_description      = local.domain_operation_description[var.operation]
    resource_lease_days       = local.domain_lease_days[var.operation]
    resource_path             = join("/", [var.topdomain, var.domain, coalesce(var.subdomain, "·")])
}

resource "vra7_deployment" "secrets-keeper-instance" {
    catalog_item_id            = local.resource_vmware_vra_token
    description                = "INFO: ${local.resource_description} on ${local.resource_path}/${local.resource_name}"
    deployment_configuration = {
        _leaseDays             = local.resource_lease_days
    }
    resource_configuration {
        component_name         = local.resource_operation
        configuration = {
            "allowrange"       = var.allow_range,
            "app"              = local.resource_name,
            "domain"           = var.domain,
            "environment"      = var.environment,
            "subdomain"        = var.subdomain,
            "topdomain"        = var.topdomain
        }
   }
    wait_timeout               = 60
}
