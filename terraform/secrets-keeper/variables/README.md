# execute¹ the command bellow as demanded from the "${aws-newcastle-environment-project-root-folder}/pagcloud/secrets-keeper" directory:

## To create a new secrets-keeper instance:
```
terraform [init|plan|apply] \ # execute the piped values in declared order
    -var="environment=[Dev|QA|Prod]" \ #choose one of the piped values
    -var="operation=register" \
    -var-file="${team-project-root-folder}/terraform/secrets-keeper/variables/commons.tfvars" 
```

# before grant write permissions remove all reference to the terraform state! !!!!!!!!!!! CHECAR SEMPRE !!!!

## To grant write permission to an already existente secrets-keeper instance for a 24h period:
```
terraform [init|plan|apply] \ # execute the piped values in declared order
    -var="environment=[Dev|QA|Prod]" \ #choose one of the piped values
    -var="operation=grant-permission" \
    -var-file="${team-project-root-folder}/terraform/secrets-keeper/variables/commons.tfvars" 
```

#Attention!!!
## ¹: the command must be executed as one line only to work, so format it before run!!!
