# provision needed s3 bucket for main tf


# get region from aws cli
TF_VAR_region="eu-west-1"

# create s3 bucket for terraform state
TF_VAR_s3_bucket_name="terraform-state-$TF_VAR_region-id-music-prod"
echo "Creating s3 bucket $TF_VAR_s3_bucket_name in region $TF_VAR_region"
aws s3api create-bucket --bucket $TF_VAR_s3_bucket_name --region $TF_VAR_region --create-bucket-configuration LocationConstraint=$TF_VAR_region

# create dynamodb table for terraform state lock
TF_VAR_dynamodb_table_name="terraform-state-lock-$TF_VAR_region"
echo "Creating dynamodb table $TF_VAR_dynamodb_table_name in region $TF_VAR_region"
aws dynamodb create-table --table-name $TF_VAR_dynamodb_table_name --attribute-definitions AttributeName=LockID,AttributeType=S --key-schema AttributeName=LockID,KeyType=HASH --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 --region $TF_VAR_region

