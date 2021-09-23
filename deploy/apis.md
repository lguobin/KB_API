KB_iTest API Document
 - **Version** 1.0
---
 - **更新说明**
```js
* 加入批量用例导入功能(2021年9月18日 14:08:28)
* 新加入场景设计与执行(2021年9月13日 10:44:55)
* 加入定时任务监听处理，用户获取token权限优化
* 测试报告增加三类搜索条件
* 加入 Mock Server 丐版
* 加入全局变量查看接口
* 加入全局变量创建&替换参数（参数化）
* 加入全局搜索接口
```
---
[toc]
---
# API Info
```js
const VERSION = '1.0.0';
const BUILD = 1;
const HOST = 'http://{ip:port}/api/${Function}';
```
---
## Headers (整体身份验证控制)
---
Header:
| 字段 | 类型 | 描述 |
|:-------------:|:-------------|
| Content-Type | String | application/json |
| Authorization | String | JWT <access_token> (注意："JWT" + <空格> + <access_token>) |
| Authorization | - | 登录接口不需要该参数 |

Success-Response:
```json
{
    "status": "ok",
    "access_token": "access_token"
}
```
Error-Response:
```json
{
    "code": "code",
    "data": "message"
}
```

---
## 用户注册&登录
---
### 用户注册
URL地址：/api/user/register
请求方式：POST
请求参数：
| 字段 | 类型 | 描述 |
|:-------------:|:-------------|
| user | String | 名字(必填) |
| password | String | 密码(必填)长度：六位以上 |
| email | String | 用户邮箱(必填)，首次注册需要激活 |
| nickname | String | 用户昵称 |
* 例子:
```json
{
    "user":"admin",
    "password":"admin",
    "email":"",
    "nickname":""
}
```
Success-Response:
```json
{
    "status": "ok",
    "access_token": "access_token"
}
```
Error-Response:
```json
{
    "code": "code",
    "data": "message"
}
```
---

### 登录接口
URL地址：/api/user/login
请求方式：POST
请求参数：
| 字段 | 类型 | 描述 |
|:-------------:|:-------------|
| user | String | 名字(必填) |
| password | String | 密码(必填) |
* 例子:
```json
{"user":"admin","password":"admin"}
```
Success-Response:
```json
{
    "status": "ok",
    "access_token": "access_token"
}
```
Error-Response:
```json
{
    "code": "code",
    "data": "message"
}
```
---
### 获取用户信息
URL地址：/api/user/getuser/<string:object_id>
请求方式：GET
请求参数：
| 字段 | 类型 | 描述 |
|:-------------:|:-------------|
| object_id | String | 用户object_id(必填) |
* 例子:
```json
{}
```
Success-Response:
```json
{
    "status": "ok",
    "user_object_id": object_id,
    "user": user,
    "nickname": nickname,
    "email": email,
    "role_id": role_id,
}
```
Error-Response:
```json
{
    "code": "code",
    "data": "message"
}
```
---

### 修改用户信息
URL地址：/api/user/modify/<string:object_id>
请求方式：PUT
请求参数：
| 字段 | 类型 | 描述 |
|:-------------:|:-------------|
| password | String | 密码(必填) |
| nickname | String | 昵称 |
| email | String | 收件邮箱 |
* 例子:
```json
{
    "password":"admin",
    "nickname":"",
    "email":""
}
```
Success-Response:
```json
{
    "status": "ok",
    "user_object_id": object_id,
    "user": user,
    "nickname": nickname,
    "email": email,
    "role_id": role_id,
}
```
Error-Response:
```json
{
    "code": "code",
    "data": "message"
}
```
---
### 刷新TOKEN
URL地址：/token/update
请求方式：POST
请求参数：
- 传空 json
| 字段 | 类型 | 描述 |
|:-------------:|:-------------|
| - | - | - |
Success-Response:
```json
{
    "status": "ok",
    "access_token": "access_token"
}
```
Error-Response:
```json
{
    "code": "code",
    "data": "message"
}
```
---
### 用户信息查看与管理
URL地址：/api/userlist
请求方式：PUT
权限：Admin 权限

| 字段 | 类型 | 描述 |
|:-------------:|:-------------|--------------|
| object_id | String | 用户OBJ_ID |
| Option | String | 操作选项 |
| Option参数说明 | - | Option参数说明 |
| adduser | Json | admin添加用户 |
| modifyuser | Json | admin修改用户信息(与adduser用法差不多) |
| reset_password | - | 重置密码为：123456 |
| delete | - | 禁用用户登录 |
---
用法：
```json
GET  http://{ip:port}/api/userlist
response:
{
    "total": 共多少条记录,
    "page": 当前第几页,
    "per_page": 每页多少条记录,
    "pages": 共多少页,
    "results": [
        数据详情 - 所有字段与 POST 请求的参数一致
    ]
}

添加用户:
PUT  http://{ip:port}/api/userlist
Body：
{
    "object_id":"be12bf63d4bd4d519c7d0e679c7ad8ab",
    "Option":"adduser",
    "adduser":{
        "user":"admin11111",
        "password":"admin11111",
        "nickname": "",
        "email": "",
        "role_id": 0,
        "confirm": 0
    }
}

reponse:
{
    "object_id": "object_id"
}

重置用户密码:
PUT  http://{ip:port}/api/userlist
Body {"object_id": "用户object_id", "Option": "reset_password"}
reponse:
{
    "data": "重置密码为: 123456",
    "status": "ok"
}

删除用户:
PUT  http://{ip:port}/api/userlist
Body {"object_id": "用户object_id", "Option": "delete"}
reponse:
{
   "object_id": "用户object_id"
}
```
---
Success-Response:
```json
{
    "status": "ok",
    "results": "results"
}
```
Error-Response:
```json
{
    "status": "failed",
    "data": "message"
}
```
---
## 搜索
URL地址：/search
请求方式：GET

| 字段 | 类型 | 描述 |
|:-------------:|:-------------|
| q | String | 搜索内容 |
Success-Response:
```json
{
    "status": "ok",
    "results": "results"
}
```
Error-Response:
```json
{
    "status": "failed",
    "data": "message"
}
```
---
## 测试报告搜索
URL地址：/searchreport
请求方式：GET

| 字段 | 类型 | 描述 |
|:-------------:|:-------------|
| Project | String | 项目object_id |
| executionMode | String | 手动（manual）或 定时（cronJob） |
| uid | String | 创建测试报告的用户object_id |
Success-Response:
```json
{
    "report": [...],
    "status": "ok"
}
```
Error-Response:
```json
{
    "status": "failed",
    "data": "message"
}
```
---
## 获取所有全局变量列表
URL地址：/<String:env_object_id>/globalParams
请求方式：GET
| 字段 | 类型 | 描述 |
|:-------------:|:-------------|
| env_object_id | String | 环境变量的 object_id(必填) |
Success-Response:
```json
{
    "status": "ok",
    "getparams": "getparams"
}
```
Error-Response:
```json
{
    "status": "failed",
    "data": "message"
}
```
---
## 手动加入全局变量
---
URL地址：/<String:env_object_id>/globalParams
请求方式：POST
| 字段 | 类型 | 描述 |
|:-------------:|:-------------|
| env_object_id | String | 环境变量的 object_id(必填) |
| name | String | 变量名字(必填) |
| value | String | 变量值 |
| uid | String | 用户object_ID(必填) |

会在 redis 中创建
    keys 名为: "手动添加_｛变量名｝_｛添加者｝的参数
---
## 收件人邮件管理
---
### 获取收件人邮件组信息
URL地址：/email
请求方式：GET
Success-Response:
```json
{
    "total": 共多少条记录,
    "page": 当前第几页,
    "per_page": 每页多少条记录,
    "pages": 共多少页,
    "results": [
        数据详情 - 所有字段与 POST 请求的参数一致，不再叙述
    ]
}
```
Error-Response:
```json
{
    "status": "failed",
    "data": "message"
}
```

### 添加、修改、删除收件人邮件组
URL地址：/addemail、/putemail/<string:object_id>、/delemail/<string:object_id>
请求方式：POST、PUT、DEL
- DEL 请求类型直接传空json

| 字段 | 类型 | 描述 |
|:-------------:|:-------------|
| name | String | 收件组名字(必填) |
| uid | String | 用户ID(必填) |
| email | String | 通过该邮箱发送(必填) |
| mailGroup | String | 收件人邮件地址(必填) |

* 例子:
```json
{
    "uid":"1@1.cn",
    "name":"测试组",
    "email":"通过该邮箱发送",
    "mailGroup":"['邮箱地址 - A', '邮箱地址 - B']"
}
```

Success-Response:
```json
{
    "object_id": "object_id"
}
```
Error-Response:
```json
{
    "status": "failed",
    "data": "message"
}
```
---
***************************************************************************
## 环境管理
---
### 获取环境变量
URL地址：/env
请求方式：GET
Success-Response:
```json
{
    "total": 共多少条记录,
    "page": 当前第几页,
    "per_page": 每页多少条记录,
    "pages": 共多少页,
    "results": [
        数据详情 - 所有字段与 POST 请求的参数一致，不再叙述
    ]
}
```
Error-Response:
```json
{
    "status": "failed",
    "data": "message"
}
```
### 添加、修改、删除环境
URL地址：/addenv、/putenv/<string:object_id>、/delenv/<string:object_id>
请求方式：POST、PUT、DEL
- DEL 请求类型直接传空json
| 字段 | 类型 | 描述 |
|:-------------:|:-------------|
| name | String | 环境名(必填) |
| uid | String | 用户ID(必填) |
| domain | String | 域名(必填) |
| projectTestType | String | 接口类型(必填) |
| redis | JSON | redis连接方式（启用全局变量必填） |
| mysql | JSON | mysql连接方式 |
| description | String | 描述信息 |
* 例子:
```json
{
    "name":"AAAAA",
    "projectTestType":1,
    "domain":"http://test-api.inmeng.vip",
    "mysql":"",
    "redis":
        {
            "host":"192.168.2.139",
            "port":16702,
            "db":3,
            "password":"redis#web~~"
        },
    "uid":"张三",
    "description":"描述一大堆东西"
}
```

Success-Response:
```json
{
    "object_id": "object_id"
}
```
Error-Response:
```json
{
    "status": "failed",
    "data": "message"
}
```
---
## 项目管理
---
### 获取项目
URL地址：/project
请求方式：GET
Success-Response:
```json
{
    "total": 共多少条记录,
    "page": 当前第几页,
    "per_page": 每页多少条记录,
    "pages": 共多少页,
    "results": [
        数据详情 - 所有字段与 POST 请求的参数一致，不再叙述
    ]
}
```
Error-Response:
```json
{
    "status": "failed",
    "data": "message"
}
```
---
### 获取项目下的所有接口信息
URL地址：/checkinterface/<string:object_id>
请求方式：GET
Success-Response:
```json
{
    "total": 共多少条记录,
    "page": 当前第几页,
    "per_page": 每页多少条记录,
    "pages": 共多少页,
    "results": [
        数据详情 - 所有字段与 POST 请求的参数一致，不再叙述
    ]
}
```
Error-Response:
```json
{
    "status": "failed",
    "data": "message"
}
```
---
### 添加、修改、删除项目
URL地址：/addProject、/putProject/<string:object_id>、/deleteProject/<string:object_id>
请求方式：POST、PUT、DEL
请求参数：
- DEL 请求类型直接传空json
| 字段 | 类型 | 描述 |
|:-------------:|:-------------|
| name | String | 项目名 |
| uid | String | 用户ID(必填) |
| projectTestType | String | 项目测试类型(必填), 传个:HTTP |
| version | String | 项目版本(必填) |
| description | String | 描述信息 |
* 例子:
```json
{
    "name":"test",
    "version":"test",
    "uid":"1@1.cn",
    "description":"descriptionasdasdaasasd",
    "projectTestType":"HTTP",
    "state":1
}
```

Success-Response:
```json
{
    "object_id": "object_id"
}
```
Error-Response:
```json
{
    "status": "failed",
    "data": "message"
}
```
---
## 接口管理
---
### 获取接口信息
URL地址：/inters
请求方式：GET
Success-Response:
```json
{
    "total": 共多少条记录,
    "page": 当前第几页,
    "per_page": 每页多少条记录,
    "pages": 共多少页,
    "results": [
        数据详情 - 所有字段与 POST 请求的参数一致，不再叙述
    ]
}
```
Error-Response:
```json
{
    "status": "failed",
    "data": "message"
}
```
---
### 获取接口下的所有用例信息
URL地址：/checkcase/<string:object_id>
请求方式：GET
Success-Response:
```json
{
    "total": 共多少条记录,
    "page": 当前第几页,
    "per_page": 每页多少条记录,
    "pages": 共多少页,
    "results": [
        数据详情 - 所有字段与 POST 请求的参数一致，不再叙述
    ]
}
```
Error-Response:
```json
{
    "status": "failed",
    "data": "message"
}
```
---
### 添加、修改、删除接口
URL地址：/addinter、/putinter/<string:object_id>、/deleteinter/<string:object_id>
请求方式：POST、PUT、DEL
请求参数：
- DEL 请求类型直接传空json
| 字段 | 类型 | 描述 |
|:-------------:|:-------------|
| name | String | 接口名(必填) |
| pid | String | 归属项目(必填) |
| uid | String | 用户ID(必填) |
| i_type | String | 接口类型(必填)、"如：HTTP、HTTPS、FTP" |
| route | String | 接口详细地址(必填) |
| headers | String | 请求头(必填) |
| requestMethod | String | 请求方法(必填) |
| delay | Int | 延时请求 |
| description | String | 描述信息 |
* 例子:
```json
{
    "name":"测试名称",
    "pid":"所属项目",
    "i_type":"http",
    "route":"/shopadm/auth/shop-token",
    "headers":"{}",
    "requestMethod":"POST",
    "delay":0,
    "uid":"1@1.cn",
    "description":"测试名称"
}
```

Success-Response:
```json
{
    "object_id": "object_id"
}
```
Error-Response:
```json
{
    "status": "failed",
    "data": "message"
}
```
---
---
## 用例模板下载、批量导入
---
### 用例模板下载
URL地址：/export_csvDemo
请求方式：GET
Success-Response:
```json
{
    【文件流，通过浏览器或其他下载工具把 csv 文件保存在本地】
}
---
### 用例模板导入
URL地址：/inputTestCases
请求方式：POST
| 字段 | 类型 | 描述 |
|:-------------:|:-------------|
| uid | String | 用户object_ID(必填) |
| files | Files | 文件流，就是下载的csv文件(必填) |
Success-Response:
​```json
{
    "msg": "导入成功"
}
​```
---
## 用例管理
---
### 获取用例信息
URL地址：/tcase
请求方式：GET
Success-Response:
​```json
{
    "total": 共多少条记录,
    "page": 当前第几页,
    "per_page": 每页多少条记录,
    "pages": 共多少页,
    "results": [
        数据详情 - 所有字段与 POST 请求的参数一致，不再叙述
    ]
}
```
Error-Response:
```json
{
    "status": "failed",
    "data": "message"
}
```
---
### 添加、修改、删除用例
URL地址：/addcase、/putcase/<string:object_id>、/delcase/<string:object_id>
请求方式：POST、PUT、DEL
请求参数：
- DEL 请求类型直接传空json
| 字段 | 类型 | 描述 |
|:-------------:|:-------------|
| name | String | 用例名(必填) |
| pid | String | 归属项目(必填) |
| Iid | String | 归属接口(必填) |
| uid | String | 用户ID(必填) |
| route | String | 接口详细地址(必填) |
| headers | list - String | 用例请求头(必填) |
| requestMethod | String | 用例请求方式(必填) |
| requestBody | list - String | 用例请求体(必填), 无则传空字符串 |
| setGlobalVars | list - String | （选填）只要有值就可以实现全局变量，设置：[{"name": "变量名", "query": ["返回值id"]}] |
| 在Body中使用全局变量方法 | String | 例子：{"token": "${变量名}"} |
| parameterType | String | 用例请求体类型(必填), 如：json、from、file |
| checkoptions | Int | 断言开关(选填-校验 response) |
| checkSpendSeconds | Float | 限定接口返回时间，如果超过该时间表示测试不通过 |
| checkResponseCode | Int | 验证接口返回状态码 |
| checkResponseBody | String | 验证接口返回体是否存在该值 |
| 使用方法 | list - String | 例子：[{"regex": "检查参数", "query": ["响应体参数"]}] |
| optionsValue | String | 对应上述描述保存对应的values |
| generate_params | String | 生成参数条件 |
| delay | Int | 延时请求 |
| variable_1 | String | 临时缓存信息1 |
| variable_1 | String | 临时缓存信息2 |
| filePath | String | 文件路径 |
| description | String | 描述信息 |

* 例子:
```json
{
    "name":"测试用例AAA",
    "pid":"归属项目",
    "Iid":"归属接口",
    "route":"/shopadm/auth/shop-token",
    "headers":[
        {
            "Content-Type":"application/json"
        }
    ],
    "requestMethod":"POST",
    "requestBody":[
        {
            "auth_type":"pwd",
            "username":"testadminwuyling",
            "password":"123456",
            "noncestr":"DQdwmgUBSPiLdYJB",
            "validation":1,
            "timestamp":1628042818,
            "vs":"984265d028fed3507e759eb3eadec944"
        }
    ],
    "setGlobalVars": [{}],
    "checkoptions ": 0,
    "checkSpendSeconds": 0.00001,
    "checkResponseCode": 666,
    "checkResponseBody": [{"regex": "检查参数", "query": ["响应体参数"]}],
    "optionsValue":"",
    "generate_params": "",
    "delay":1,
    "variable_1":"",
    "variable_2":"",
    "uid":"张三",
    "description":"测试用例",
    "parameterType":"json",
    "filePath":"pwd"
}
```

Success-Response:
```json
{
    "object_id": "object_id"
}
```
Error-Response:
```json
{
    "status": "failed",
    "data": "message"
}
```
---
## 单步调试
---
### 单个用例调试（异步执行）
URL地址：/ByDebug
请求方式：POST
请求参数：
- DEL 请求类型直接传空json
| 字段 | 类型 | 描述 |
|:-------------:|:-------------|
| CaseList | List-String | (必填)用例object-id，可一个或多个 |
| EnvId | String | (必填)环境变量object-id |
| uid | String | 用户id(必填) |
| executionMode | String | manual(固定参数) |

* 例子:
```json
{
    "CaseList":[
        "7a51834824a3456faf6e0135489ebc3f",
        "8c947bb9ac9c4ccab4b382c18644f2f0",
        "610cfcd215200abc48507cbb"
    ],
    "EnvId":"fce67bb495534c4d81152696885b44a1",
    "uid":"1@1.cn",
    "executionMode":"manual"
}
```
Success-Response:
```json
{
    "status": "ok",
    "data": "测试完毕, 稍后前往「DebugLastResult」中获取结果",
    
}
```
Error-Response:
```json
{
    "status": "failed",
    "data": "message"
}
```
---
### 获取测试用例结果
URL地址：/DebugLastResult/<string:object_id>
请求方式：GET
Success-Response:
```json
{
    "status": "ok",
    "result": {
        EnvId              -> 环境变量的 object_ID
        EnvName            -> 环境变量的名字
        report_object_id   -> 测试报告的 object_ID
        Project_id         -> 归属项目的 object_ID
        create_at          -> 报告的创建时间
        updated_at         -> 报告的修改时间
        StartTime          -> 启动的测试时间戳
        executionMode      -> 测试模式（cronJob为定时、manual为手动调试、scenes为场景）
        cronJobId          -> 定时服务id（没有默认为 null）
        totalCount         -> 执行测试用例的总数
        passCount          -> 执行测试用例通过数量
        failCount          -> 执行测试用例失败数量
        errorCount         -> 执行测试用例错误数量
        spendTimeInSec     -> 整体耗时
        uid                -> 创建报告的人员 object_ID
        interfaces_Suites_CaseDetail  -> 接口测试详情数组{
            75cc456d9c4d41f6980e02f46d611a55 -> 接口的object_ID{
                Conclusion -> 结论（通过或失败）[reason：有详细说明成功或失败]
                Project_id -> 用例归属的项目 object_ID
                Interface_id -> 用例归属的接口 object_ID
                object_id -> 测试用例自身的 object_id
                elapsedSeconds -> 单个用例请求的耗时（浮点数）
                responseData -> 测试用例响应体
                responseStatusCode -> 测试用例响应代码
                status -> 用例测试结果(pass\fail\error)
                test_CaseDetail -> 用例请求详情{
                    requestBody -> 请求体
                    requestMethod -> 请求方式
                    URL-> 请求地址
                    delaySeconds(预留、暂时不用管这参数)
                }
                
                testStartTime （暂时废弃）
                spendTimeInSec（暂时废弃）
                dataInitResult -> 数据初始化结果（预留、暂时不用管这参数）
                checkoptions -> 用例断言开关（开启情况下会判断以下参数，关闭则不会处理以下参数）
                checkSpendSeconds -> 判断用例响应运行时间能否在规定时间运行完毕
                checkResponseCode -> 判断用例的HTTP code
                checkResponseBody -> 判断用例的返回值断言（用法与测试用例参数一致，详情参考测试用例参数表）
            }
        }
    }
}
```
Error-Response:
```json
{
    "status": "failed",
    "data": "message"
}
```
---
### 接口用例调试（异步执行）
URL地址：/ByInterface
请求方式：POST
请求参数：
- DEL 请求类型直接传空json
| 字段 | 类型 | 描述 |
|:-------------:|:-------------|
| Interface | List-String | (必填)接口object-id，可一个或多个 |
| EnvId | String | (必填)环境变量object-id |
| ProjectId | String | (必填)归属项目object-id |
| uid | String | 用户id(必填) |
| executionMode | String | manual(固定参数) |
* 例子:
```json
{
    "Interface":[
        "75cc456d9c4d41f6980e02f46d611a5c",
        "75cc456d9c4d41f6980e02f46d611a55"
    ],
    "EnvId":"9d289cf07b244c91b81ce6bb54f2d627",
    "ProjectId":"c3009c8e62544a23ba894fe5519a6b64",
    "uid":"1@1.cn",
    "executionMode":"manual"
}
```
Success-Response:
```json
{
    "status": "ok",
    "data": "测试完毕, 稍后前往「测试报告」查看结果",
    
}
```
Error-Response:
```json
{
    "status": "failed",
    "data": "message"
}
```
---
## 查看测试报告
---
### 获取测试报告
URL地址：/report
请求方式：GET
Success-Response:
```json
{
    "total": 共多少条记录,
    "page": 当前第几页,
    "per_page": 每页多少条记录,
    "pages": 共多少页,
    "results": [
        展示测试报告的 list｛
            EnvId -> 环境变量的 object_ID
            EnvName -> 环境变量的名字
            report_object_id   -> 测试报告的 object_ID
            Project_id         -> 归属项目的 object_ID
            create_at          -> 报告的创建时间
            updated_at         -> 报告的修改时间
            StartTime          -> 启动的测试时间戳
            executionMode      -> 测试模式（cronJob为定时、manual为手动调试、scenes为场景）
            cronJobId          -> 定时服务id（没有默认为 null）
            totalCount         -> 执行测试用例的总数
            passCount          -> 执行测试用例通过数量
            failCount          -> 执行测试用例失败数量
            errorCount         -> 执行测试用例错误数量
            spendTimeInSec     -> 整体耗时
            uid                -> 创建报告的人员 object_ID
        ｝
    ]
}
```
Error-Response:
```json
{
    "status": "failed",
    "data": "message"
}
```
---
### 获取测试报告 - 详情
URL地址：/report/<string:report_object_id>
请求方式：GET
Success-Response:
```json
{
    EnvId              -> 环境变量的 object_ID
    EnvName            -> 环境变量的名字
    report_object_id   -> 测试报告的 object_ID
    Project_id         -> 归属项目的 object_ID
    create_at          -> 报告的创建时间
    updated_at         -> 报告的修改时间
    StartTime          -> 启动的测试时间戳
    executionMode      -> 测试模式（cronJob为定时、manual为手动调试、scenes为场景）
    cronJobId          -> 定时服务id（没有默认为 null）
    totalCount         -> 执行测试用例的总数
    passCount          -> 执行测试用例通过数量
    failCount          -> 执行测试用例失败数量
    errorCount         -> 执行测试用例错误数量
    spendTimeInSec     -> 整体耗时
    uid                -> 创建报告的人员 object_ID
    interfaces_Suites_CaseDetail  -> 接口测试详情数组{
        75cc456d9c4d41f6980e02f46d611a55 -> 接口的object_ID{
            Conclusion -> 结论（通过或失败）[reason：有详细说明成功或失败]
            Project_id -> 用例归属的项目 object_ID
            Interface_id -> 用例归属的接口 object_ID
            object_id -> 测试用例自身的 object_id
            elapsedSeconds -> 单个用例请求的耗时（浮点数）
            responseData -> 测试用例响应体
            responseStatusCode -> 测试用例响应代码
            status -> 用例测试结果(pass\fail\error)
            test_CaseDetail -> 用例请求详情{
                requestBody -> 请求体
                requestMethod -> 请求方式
                URL-> 请求地址
                delaySeconds(预留、暂时不用管这参数)
            }
            
            testStartTime （暂时废弃）
            spendTimeInSec（暂时废弃）
            dataInitResult -> 数据初始化结果（预留、暂时不用管这参数）
            checkoptions -> 用例断言开关（开启情况下会判断以下参数，关闭则不会处理以下参数）
            checkSpendSeconds -> 判断用例响应运行时间能否在规定时间运行完毕
            checkResponseCode -> 判断用例的HTTP code
            checkResponseBody -> 判断用例的返回值断言（用法与测试用例参数一致，详情参考测试用例参数表）
        }
    }
}
```
Error-Response:
```json
{
    "status": "failed",
    "data": "message"
}
```
---
### 清理测试报告
URL地址：/cleanReports
请求方式：POST
请求参数：
- DEL 请求类型直接传空json
| 字段 | 类型 | 描述 |
|:-------------:|:-------------|
| cleanDate | Int | 天数，0：清除所有报告,7:表示删除前7天的报告 |
| projectId | Sting | 归属项目ID |
| operator | Sting | 操作用户ID |
| executionMode | Sting | manual（预留参数） |

* 例子:
```json
{
    "cleanDate":0,
    "projectId":"6110e55b78f5bbbe3d9e2a6c",
    "operator":"1@1.cn",
    "executionMode":"manual"
}
```
Success-Response:
```json
{
    "status": "ok"，
    "data": "删除报告成功"
}
```
Error-Response:
```json
{
    "status": "failed",
    "data": "message"
}
```
---
## 定时任务
---
### 获取任务列表
URL地址：/cronjob
请求方式：GET

Success-Response:
```json
{
    "total": 共多少条记录,
    "page": 当前第几页,
    "per_page": 每页多少条记录,
    "pages": 共多少页,
    "results": [
        数据内容
    ]
}
```
Error-Response:
```json
{
    "code": "code",
    "data": "message"
}
```
---
### 添加、修改、删除任务
URL地址：/addcron、/putcron/<string:object_id>、/delcron/<string:object_id>
请求方式：POST、PUT、DEL
请求参数：
- DEL 请求类型直接传空json
| 字段 | 类型 | 描述 |
|:-------------:|:-------------|
| mission_name | String | 定时服务名字(必填) |
| uid | String | 操作用户ID(必填) |
| EnvId | String | 使用环境(必填) |
| pid | String | 归属项目(选填) |
| SuiteIdList | list - String | 归属接口下的所有用例(选填) |
| triggerType | OBJ | (必填)"interval"或"runDate"参数二选一, interval：间隔时间；runDate：一次性定期任务 |
| interval | Int | 时间单位：秒(必填) |
| runDate | LongInt | 时间戳(必填) |
| alwaysSendMail | Boolean | 是否发送邮件（false：标识关闭，true 标识发送） |
| alarmMailGroupList | OBJ | 收件人邮件组object_id，支持多个邮件组 |
| alwaysWXWorkNotify | Boolean | 是否发送企微消息（false：标识关闭，true 标识发送） |

* 例子:
```json
{
    "uid": "张三",
    "mission_name": "定时服务名字",
    "pid": "c3009c8e62544a23ba894fe5519a6b64",
    "EnvId": "9d289cf07b244c91b81ce6bb54f2d627",
    "SuiteIdList": ["75cc456d9c4d41f6980e02f46d611a5c"],
    "triggerType": "interval",
    "runDate": 1239863854,
    "interval": 43201,
    "alwaysSendMail": true,
    "alwaysWXWorkNotify": true,
    "alarmMailGroupList": "['4dc0e648e61846a4aca01421aa1202e2', '2222222222222']"
}
```

Success-Response:
```json
{
    "object_id": "object_id"
}
```
Error-Response:
```json
{
    "status": "failed",
    "data": "message"
}
```
---
### 暂停与启动任务
URL地址：/nodifycron/<string:object_id>
请求方式：POST
请求参数：
| 字段 | 类型 | 描述 |
|:-------------:|:-------------|
| object_id | String | 创建任务返回的object_id |
| nodify | Int | 0标识恢复任务，1表示暂停任务 |
* 例子:
```json
{"nodify": 0}
```
---
### 查看所有任务信息、暂停、恢复、删除（只有管理员有该权限）
URL地址：/api/Taskslist
请求方式：POST
请求参数：
| 字段 | 类型 | 描述 |
|:-------------:|:-------------|
| mission | String | 创建任务时候的名字 |
| TaskOption | String | 操作该任务的方式 |
| pause | String | 暂停任务 |
| resume | String | 恢复任务 |
| dels | String | 删除任务 |
| delall | String | 删除所有任务 |
| jobs | String | 列出现所有任务 |

* 例子:
```json
{"mission":"创建任务时候的名字", "TaskOption":"jobs"}
```

Success-Response:
```json
{
    "jobs": "[]"
}
```
---
## 场景模式
---
### 获取场景列表
URL地址：/scenes
请求方式：GET
Success-Response:
```json
{
    "total": 共多少条记录,
    "page": 当前第几页,
    "per_page": 每页多少条记录,
    "pages": 共多少页,
    "results": [
        数据内容
    ]
}
```
Error-Response:
```json
{
    "status": "failed",
    "data": "message"
}
```
---
### 获取场景列表
URL地址：/scenes、/scenes/<string:object_id>、/scenes/<string:object_id>
请求方式：POST、PUT、DEL
请求参数：
| 字段 | 类型 | 描述 |
|:-------------:|:-------------|
| name | String | 场景名字(必填) |
| uid| String | 操作员(必填) |
| TCase_ids | list - String | 场景涉及到的用例(必填，有序从上到下执行，传参注意) |
| TCase_ids | 说明 | 如例子所示，传参注意值为有序队列，先进先走，会影响后续的结果 |
| run_state | Int | 默认为关闭状态，0为关闭状态，1为启动状态 |
| description | String | 描述 |
* 例子:
```json
{
    "name": "场景名字",
    "uid": "asdasdas",
    "TCase_ids": [{"EnvId":"AA环境", "场景":[1,2,3,4]}, {"EnvId":"BBB环境", "场景":[1,2,3,4]}],
    "run_state": 0,
    "description": "asdadasdasaasdasasdadadsadadadasdads"
}
```
### 激活场景
URL地址：/scenes/activation/<string:object_id>
请求方式：POST
请求参数：
| 字段 | 类型 | 描述 |
|:-------------:|:-------------|
| activation | String | 场景的object-ID(必填) |
| uid | String | 用户的object-ID(必填) |
* 例子:
```json
{
    "activation":"0c9f14e7cbcf4986bc32f1b311ad1bff",
    "uid":11111111
}
```

---
## Mock - 丐版
---
### 说明
```json
Mock丐版支持[ GET、POST、PUT、DELETE、PATCH、HEAD、OPTIONS ]请求方式

暂只提供 application/json
默认情况下会返回 {"TryMock" : "OK"}
想改变 response 响应内容，可以在请求 Mock 接口中传入 Body，该 Body 就会当做 response 给你返回
```
---
* 例子一（不传Body）:
```json
GET http://{ip:port}/mock/<path:path>
Body: false
response: {"TryMock" : "OK"}
```
---
* 例子二（传Body）:
```json
GET http://{ip:port}/mock/<path:path>
Body: {"演示响应体": "响应结果"}
response: {"演示响应体": "响应结果"}
```
---