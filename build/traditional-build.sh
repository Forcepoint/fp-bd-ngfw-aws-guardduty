# Copy all required files to dist directory
cp $(pwd)/* $(pwd)/build/dist

# Zip the files
cd ./build/dist
zip -r ./fp-ngfw-aws-guardduty-v1.zip .

# Remove the files from dist directory
rm *.py
rm *.md
rm *.txt