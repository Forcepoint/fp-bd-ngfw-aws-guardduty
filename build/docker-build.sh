# Ask for version number. Default to latest.
echo "Which version of the integration are you building? Defaults to latest."
read version

if [[ "$version" == "" ]]; then
    version="latest"
fi

echo "Version tag selected: $version"
echo

# Ask for remote repository
echo "Which repository are you building for? Defaults to artifactory. "
echo
echo "1) Artifactory (Private)"
echo "2) Frcpnt (Public)"
echo
read repository

if [[ "$repository" == "2" ]]; then
    repository="docker.frcpnt.com"
else
    repository="forcepoint-bd-docker.jfrog.io"
fi

echo
echo "Repository selected: $repository"

# Run docker build for both images
echo "Building images..."
echo
docker build -f docker/app/Dockerfile -t $repository/ngfw-aws-guardduty-server:$version .
docker build -f docker/worker/Dockerfile -t $repository/ngfw-aws-guardduty-worker:$version .
echo

# Push images to repo
echo "Would you like to push the images to the remote repository (y/n)?"
read answer

if [[ "$answer" == "y" ]]; then
    echo
    echo "Pushing to remote respository..."
    echo
    docker push $repository/ngfw-aws-guardduty-server:$version
    docker push $repository/ngfw-aws-guardduty-worker:$version
fi
