# Sequoia API 删除货件问题解决方案

## 问题现象
调用 `DeleteShipment` 时返回错误：
```
Code: -1
Message: A delete exception occurred
delete process failed unexpectedly
```

## 问题原因
XML 命名空间写错了，看了一下你的 XSD 文件，发现命名空间不匹配：

**你现在用的：**
```xml
<shipmentIdentifier xmlns="asm.org.uk/Sequoia/ShipmentIdentifier">
```

**应该用的：**
```xml
<shipmentIdentifier xmlns="ShipmentIdentifier">
```

## 修复代码

把 `delete_shipment_demo` 函数改成这样：

```python
def delete_shipment_demo(shipment_reference):
    shipment_identifier_xml = f'''
    <shipmentIdentifier xmlns="ShipmentIdentifier"
        xmlns:xsShipmentIdentityType="asm.org.uk/Sequoia/ShipmentIdentityType">
        <shipmentIdentity>
            <shipmentReference>{shipment_reference}</shipmentReference>
        </shipmentIdentity>
    </shipmentIdentifier>
    '''
    try:
        DeleteRequest = client.get_type('ns3:DeleteRequest')
        req = DeleteRequest(
            TransactionId="delete" + shipment_reference,
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
```

## 主要修改
- 把 `xmlns="asm.org.uk/Sequoia/ShipmentIdentifier"` 改成 `xmlns="ShipmentIdentifier"`
- 加了类型命名空间声明（可选，但建议加上）

## 其他可能的问题
如果修改后还是不行，检查一下：

1. **货件是否存在** - 确认 `S25/A0652` 这个单号在系统里存在
2. **权限问题** - 检查 `operator001` 是否有删除权限
3. **货件状态** - 有些状态下的货件可能不允许删除
4. **关联数据** - 货件可能有子记录需要先删除

试试看，应该能解决问题。