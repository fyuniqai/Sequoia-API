2025-06-23 19:17:34,243 - INFO - 开始删除 shipment...
2025-06-23 19:17:34,244 - DEBUG - HTTP Post to http://localhost:9010/Asm/Sequoia/SequoiaApiSoapService:
<?xml version='1.0' encoding='utf-8'?>
<soap-env:Envelope xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/"><soap-env:Header xmlns:wsa="http://www.w3.org/2005/08/addressing"><wsa:Action>http://tempuri.org/ISequoiaApiSoapService/DeleteShipment</wsa:Action><wsa:MessageID>urn:uuid:293f4b08-4e67-44b3-82be-594f95acc1d4</wsa:MessageID><wsa:To>http://localhost:9010/Asm/Sequoia/SequoiaApiSoapService</wsa:To></soap-env:Header><soap-env:Body><ns0:DeleteShipment xmlns:ns0="http://tempuri.org/"><ns0:deleteRequest><ns1:TransactionId xmlns:ns1="http://schemas.datacontract.org/2004/07/ASM.Sequoia.Api.Contracts.DataContracts.Request">deleteS25/A0652</ns1:TransactionId><ns2:Content xmlns:ns2="http://schemas.datacontract.org/2004/07/ASM.Sequoia.Api.Contracts.DataContracts.Request">
    &lt;shipmentIdentifier xmlns="asm.org.uk/Sequoia/ShipmentIdentifier"&gt;
        &lt;shipmentIdentity&gt;
            &lt;shipmentReference&gt;S25/A0652&lt;/shipmentReference&gt;
        &lt;/shipmentIdentity&gt;
    &lt;/shipmentIdentifier&gt;

    </ns2:Content></ns0:deleteRequest></ns0:DeleteShipment></soap-env:Body></soap-env:Envelope>
2025-06-23 19:17:34,246 - DEBUG - 重写请求 URL: http://localhost:9010/Asm/Sequoia/SequoiaApiSoapService -> http://185.79.59.183:9010/Asm/Sequoia/SequoiaApiSoapService
2025-06-23 19:17:34,496 - DEBUG - http://185.79.59.183:9010 "POST /Asm/Sequoia/SequoiaApiSoapService HTTP/1.1" 200 797
2025-06-23 19:17:34,497 - DEBUG - HTTP Response from http://localhost:9010/Asm/Sequoia/SequoiaApiSoapService (status: 200):
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><DeleteShipmentResponse xmlns="http://tempuri.org/"><DeleteShipmentResult xmlns:a="http://schemas.datacontract.org/2004/07/ASM.Sequoia.Api.Contracts.DataContracts.Response" xmlns:i="http://www.w3.org/2001/XMLSchema-instance"><a:Errors><a:ErrorResponse><a:ErrorDetails><a:ErrorDetail><a:Code>-1</a:Code><a:Message>A delete exception occurred</a:Message></a:ErrorDetail></a:ErrorDetails><a:ErrorMessage>delete process failed unexpectedly.</a:ErrorMessage><a:Errors xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"><b:string>A delete exception occurred</b:string></a:Errors></a:ErrorResponse></a:Errors><a:ReturnValue>False</a:ReturnValue></DeleteShipmentResult></DeleteShipmentResponse></s:Body></s:Envelope>
2025-06-23 19:17:34,498 - INFO - DeleteShipment 返回：{
    'Errors': {
        'ErrorResponse': [
            {
                'ErrorDetails': {
                    'ErrorDetail': [
                        {
                            'Code': -1,
                            'Message': 'A delete exception occurred'
                        }
                    ]
                },
                'ErrorMessage': 'delete process failed unexpectedly.',
                'Errors': {
                    'string': [
                        'A delete exception occurred'
                    ]
                }
            }
        ]
    },
    'ReturnValue': 'False'
}