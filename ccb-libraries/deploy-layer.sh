mkdir python
mkdir python/ccb_toolbox
cp ccb_toolbox/* python/ccb_toolbox
zip -r -y ccb_toolbox.zip python/
aws s3 cp ccb_toolbox.zip s3://eyanez/ccb_toolbox.zip --region us-east-1
aws lambda publish-layer-version --layer-name ccb_toolbox --description 'Utilidades y funciones reutilizables para desarrollo python' --content S3Bucket=eyanez,S3Key=ccb_toolbox.zip --compatible-runtimes python3.8 --region us-east-1
rm -rf ccb_toolbox.zip python/
