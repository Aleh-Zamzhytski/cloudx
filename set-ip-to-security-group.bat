rem .\set-ip-to-security-group.bat <your-profile-name> <security-group-id> <region>
for /f %%a in ('powershell Invoke-RestMethod api.ipify.org') do set PublicIP=%%a
aws ec2 authorize-security-group-ingress --group-id %2 --protocol tcp --port 22 --cidr %PublicIP%/32 --profile %1 --region %3
