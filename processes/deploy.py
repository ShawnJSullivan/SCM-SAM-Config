from ftplib import FTP
import settings
from helpers import ConfigDeployer

# Setup FTP connection
ftp = FTP(settings.ftpHost, settings.ftpUser, settings.ftpPassword)
# Go to correct remote directory
ftp.cwd(settings.ftpBasePath)

# Instantiate deployment helper class
configDeployer = ConfigDeployer(ftp, settings)

# Upload the new configurations
configDeployer.deploy()

print(configDeployer.get_status())

ftp.quit()
