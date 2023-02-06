from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
import pandas as pd

#enter credentials
account_name = 'globantcoding'
account_key = '3E3DWfAcB6NcdXfol/35ZIcIDd/RQ4o7lk8xZEuDZIjtSh2lwkNVKH29f6CjtEe3EU4uIiJ0B1l7+ASthVdNmQ=='

#create a client to interact with blob storage
def createClient():
    connect_str = 'DefaultEndpointsProtocol=https;AccountName=' + account_name + ';AccountKey=' + account_key + ';EndpointSuffix=core.windows.net'
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    return blob_service_client

#use the client to connect to the container
def getContainerConnection(blobServiceClient, containerName):
    container_client = blobServiceClient.get_container_client(containerName)
    return container_client

#get a list of all blob files in the container
def getlistBlobs(containerClient):
    blob_list = []
    for blob_i in containerClient.list_blobs():
        blob_list.append(blob_i.name)
    return blob_list
    


def getDataframe(blobList,containerName):
    df_list = []
    #generate a shared access signiture for files and load them into Python
    for blob_i in blobList:
        #generate a shared access signature for each blob file
        sas_i = generate_blob_sas(account_name = account_name,
                                    container_name = containerName,
                                    blob_name = blob_i,
                                    account_key=account_key,
                                    permission=BlobSasPermissions(read=True),
                                    expiry=datetime.utcnow() + timedelta(hours=1))
        
        sas_url = 'https://' + account_name+'.blob.core.windows.net/' + containerName + '/' + blob_i + '?' + sas_i
        
        df = pd.read_csv(sas_url)
        df_list.append(df)
        
    df_combined = pd.concat(df_list, ignore_index=True)
    return df_combined