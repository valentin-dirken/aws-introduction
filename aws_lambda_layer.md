```bash
mkdir -p multi-agent-orchestrator/nodejs && cd multi-agent-orchestrator/nodejs && echo '{"private": true}' > package.json && npm install multi-agent-orchestrator && cd .. && zip -r multi-agent-orchestrator.zip nodejs
aws lambda publish-layer-version --layer-name multi-agent-orchestrator --zip-file fileb://multi-agent-orchestrator.zip
```
# Define the layer name and NPM packages
```bash
LAYER_NAME="dmit-mssql-v1"
NPM_PACKAGES="aws-sdk csv-writer fs nodemailer mssql"
```

# Create a directory for the layer
```bash
mkdir -p $LAYER_NAME/nodejs
```

# Navigate to the layer directory
```bash
cd $LAYER_NAME/nodejs
```

# Create a package.json file
```bash
echo '{"private": true}' > package.json
```

# Install the NPM packages
```bash
npm install $NPM_PACKAGES
```

# Navigate back to the parent directory
```bash
cd ..
```

# Zip the layer
```bash
zip -r $LAYER_NAME.zip nodejs
```

# Print the success message
```bash
echo "Lambda Layer $LAYER_NAME.zip created successfully."
```

# Optional: You can use AWS CLI to publish the layer
```bash
aws lambda publish-layer-version --layer-name $LAYER_NAME --zip-file fileb://$LAYER_NAME.zip
```
```
