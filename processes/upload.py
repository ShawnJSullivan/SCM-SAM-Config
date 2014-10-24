from ftplib import FTP
import settings
from helpers import ConfigDeployer

# Setup FTP connection
ftp = FTP(settings.ftpHost, settings.ftpUser, settings.ftpPassword)
# Go to correct remote directory
ftp.cwd(settings.ftpBasePath)

# Instantiate deployment helper class
configDeployer = ConfigDeployer(ftp, settings)

print(configDeployer.get_status())

# Upload the new configurations
configDeployer.upload()

ftp.quit()
