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

# Revert to the newest archived configuration
configDeployer.revert()

print(configDeployer.get_status())

ftp.quit()
