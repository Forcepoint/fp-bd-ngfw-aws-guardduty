# Set required environment variables
export CONFIG_URL=<CONFIG_URL>

# Install Python
yum install -y https://centos7.iuscommunity.org/ius-release.rpm
yum update
yum install -y python36u python36u-libs python36u-devel python36u-pip

# Install pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py

# Install python requirements
python3 -m pip install -r requirements.txt

# Install rabbitmq and all rabbitmq requirements
yum -y install epel-release
yum -y update
yum -y install erlang socat
yum -y install wget
wget https://www.rabbitmq.com/releases/rabbitmq-server/v3.6.10/rabbitmq-server-3.6.10-1.el7.noarch.rpm
rpm --import https://www.rabbitmq.com/rabbitmq-release-signing-key.asc
rpm -Uvh rabbitmq-server-3.6.10-1.el7.noarch.rpm
systemctl start rabbitmq-server
systemctl enable rabbitmq-server

# Open required port
iptables -A INPUT -m state --state NEW -p tcp --dport 5000 -j ACCEPT
service iptables save
firewall-cmd --zone=public --permanent --add-port=5000/tcp
firewall-cmd --reload

# Add route to broker in hosts file
echo "127.0.0.1   broker" >> /etc/hosts

# Create directories for files
mkdir /etc/ngfw-aws-guardduty-worker
mkdir /etc/ngfw-aws-guardduty-server

# Update file perms
chmod +x ./start_server.sh
chmod +x ./start_worker.sh

# Move files to correct location
cp -r ./* /etc/ngfw-aws-guardduty-worker
cp -r ./* /etc/ngfw-aws-guardduty-server

# Install service files
cp /etc/ngfw-aws-guardduty-worker/ngfw-aws-guardduty-worker.service /etc/systemd/system/ngfw-aws-guardduty-worker.service
cp /etc/ngfw-aws-guardduty-server/ngfw-aws-guardduty-server.service /etc/systemd/system/ngfw-aws-guardduty-server.service
chmod 644 /etc/systemd/system/ngfw-aws-guardduty-server.service
chmod 644 /etc/systemd/system/ngfw-aws-guardduty-worker.service

# Create log file
touch /etc/ngfw-aws-guardduty-server/events.log
chmod 777 /etc/ngfw-aws-guardduty-server/events.log
touch /etc/ngfw-aws-guardduty-worker/events.log
chmod 777 /etc/ngfw-aws-guardduty-worker/events.log

# Start the services
systemctl daemon-reload
systemctl start ngfw-aws-guardduty-worker
systemctl start ngfw-aws-guardduty-server
systemctl enable ngfw-aws-guardduty-worker
systemctl enable ngfw-aws-guardduty-server
