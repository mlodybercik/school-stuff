import ssl
import certifi
sslcontext = ssl.create_default_context(cafile=certifi.where())