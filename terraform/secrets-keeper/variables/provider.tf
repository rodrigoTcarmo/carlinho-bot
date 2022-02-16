locals {
    /*" Vide docs for more information:
        https://docs.cloud.intranet.pags/documentacao-api/cofre-de-segredos/criando-via-api/
        https://docs.cloud.intranet.pags/documentacao-api/cofre-de-segredos/atualizar-via-api/
    "*/
    domain_tenant_value = {
        Dev  = "pagseguro-dev"
        QA   = "pagseguro"
        Prod = "pagseguro"
    }
}

locals {
    provider_tenant_value = local.domain_tenant_value[var.environment]
}

provider "vra7" {
    username = var.user
    password = var.user_password
    tenant   = local.provider_tenant_value
    host     = "https://cloud.intranet.pags"
    insecure = var.must_ignore_invalid_ssl_certificate
}
