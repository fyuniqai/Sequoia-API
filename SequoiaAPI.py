import logging
from zeep import Client
from zeep.transports import Transport
from zeep.exceptions import Fault
import requests
from zeep.helpers import serialize_object
# 配置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class RewriteHostAdapter(requests.adapters.HTTPAdapter):
    def send(self, request, **kwargs):
        if 'localhost:9010' in request.url:
            original_url = request.url
            request.url = request.url.replace('localhost:9010', '185.79.59.183:9010')
            logging.debug("重写请求 URL: %s -> %s", original_url, request.url)
        return super().send(request, **kwargs)

# 配置 Transport
session = requests.Session()
session.mount('http://', RewriteHostAdapter())
transport = Transport(session=session)

# WSDL 地址
wsdl_url = 'http://185.79.59.183:9010/Asm/Sequoia/SequoiaApiSoapService?wsdl'
logging.debug("创建 Zeep 客户端，连接到 WSDL: %s", wsdl_url)

# 创建 zeep 客户端
client = Client(wsdl_url, transport=transport)
for service in client.wsdl.services.values():
    for port in service.ports.values():
        operations = port.binding._operations
        for operation in operations.values():
            print(f'接口名：{operation.name}') 
            print(f'输入消息：{operation.input.signature()}')
            print(f'输出消息：{operation.output.signature()}\n')


print("!!!!!!!!!!!!!!!!!",client.get_type('ns3:CreateRequest'))

# 绑定到具体服务端口（必须匹配 WSDL 定义）
service = client.bind('SequoiaApiSoapService', 'BasicHttpBinding_ISequoiaApiSoapService')



# 获取 API 版本
def get_api_version():
    try:
        logging.debug("调用 GetApiVersion 方法")
        version_response = service.GetApiVersion()
        logging.info("📦📦📦请求响应:\n %s", version_response.ReturnValue)
        return version_response
    except Fault as f:
        logging.error("❗❗❗SOAP Fault: %s", f)
    except Exception as e:
        logging.error("❗❗❗GetApiVersion 错误: %s", e)

#创建shipment
def create_shipment_demo():
    shipment_xml = '''
    <?xml version="1.0" encoding="utf-8"?>
    <shipment xmlns="Shipment"
        xmlns:xsPort="asm.org.uk/Sequoia/UnLocation"
        xmlns:xsAccount="asm.org.uk/Sequoia/Account"
        xmlns:xsAirShipment="asm.org.uk/Sequoia/AirShipment"
        xmlns:xsOceanShipment="asm.org.uk/Sequoia/OceanShipment"
        xmlns:xsRoadShipment="asm.org.uk/Sequoia/RoadShipment"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="asm.org.uk/Sequoia/Shipment shipment.xsd">
    
    <shipmentType>OI</shipmentType> 
    <shipmentCategory>OM</shipmentCategory> 
    
    <!-- Origin & Destination -->
    <originPort>
        <code>CNNBP</code>
        <name>Ningbo Port</name>
        <country>CN</country>
    </originPort>
    <destinationPort>
        <code>GBFXT</code>
        <name>Felixstowe</name>
        <country>GB</country>
    </destinationPort>

    <!-- Customer Info -->
    <consignor>
        <code>SHIPPER001</code>
        <name>Shipper Company Ltd</name>
    </consignor>
    <consignee>
        <code>RECEIVER001</code>
        <name>Receiver Company Ltd</name>
    </consignee>

    <!-- Shipment Type Detail -->


    <!-- Master B/L -->
    <master>ABCD012345</master>

    <!-- Container Numbers -->
    <containers>
        <containerNumber>ABCD012345</containerNumber>
    </containers>

    <!-- Packages -->
    <packages>50</packages>

    </shipment>


    '''
    try:
        CreateRequest = client.get_type('ns3:CreateRequest')
        req = CreateRequest(
            TransactionId="20240610002",
            ImpersonationContextId="operator001",
            Content=shipment_xml
        )
        result = service.CreateShipment(createRequest=req)
        logging.info("CreateShipment 返回：%s", result)
    except Fault as f:
        logging.error("SOAP fault: %s", f)
    except Exception as e:
        logging.error("请求错误: %s", e)



# 删除 shipment
def delete_shipment_demo(shipment_reference):
    """
    调用 DeleteShipment API 删除指定 shipment_reference 的货件。
    :param shipment_reference: 要删除的货件的 shipmentReference（唯一单号）
    """
    shipment_identifier_xml = f'''
    <shipmentIdentifier xmlns="asm.org.uk/Sequoia/ShipmentIdentifier">
        <shipmentIdentity>
            <shipmentReference>{shipment_reference}</shipmentReference>
        </shipmentIdentity>
    </shipmentIdentifier>
    
    '''
    try:
        DeleteRequest = client.get_type('ns3:DeleteRequest')
        req = DeleteRequest(
            TransactionId="delete" + shipment_reference,  # 每次唯一，建议加前缀
            Content=shipment_identifier_xml
        )
        result = service.DeleteShipment(deleteRequest=req)
        logging.info("DeleteShipment 返回：%s", result)
        return result
    except Fault as f:
        logging.error("SOAP fault: %s", f)
    except Exception as e:
        logging.error("DeleteShipment 错误: %s", e)
    return None  


# 示例调用
if __name__ == '__main__':
    # 获取 API 版本
    # get_api_version()
    # 调用 create_shipment
    # logging.info("开始创建 shipment...")
    # create_shipment_demo()
    logging.info("开始删除 shipment...")
    delete_shipment_demo("S25/A0652")