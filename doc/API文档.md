# API文档

目前的后端API分为用户部分和项目部分。

用户部分的API接口如下：
* [用户注册](#用户注册)
* [用户登录](#用户登录)
* [用户退出登录](#用户退出登录)
* [列出所有项目](#列出所有项目)
* [创建项目](#创建项目)
* [删除项目](#删除项目)

项目部分的API接口如下：
* [列出所有文件](#列出所有文件)
* [创建文件](#创建文件)
* [删除文件](#删除文件)
* [创建文件夹](#创建文件夹)
* [删除文件夹](#删除文件夹)
* [上传文件](#上传文件)
* [下载文件](#下载文件)

管理员页面的API接口如下：
* [请求所有用户名下的所有项目](#请求所有用户名下的所有项目)
* [请求项目日志](#请求项目日志)


各API的具体文档如下：

## 用户注册

**接口：** `[POST] /user/register`

**请求：** json对象，具体格式为：
```json
{
    "username": "xxx",
    "password": "xxx"
}
```
| 名称 | 类型 | 描述 |
| - | - | - |
| username | string | 新用户的用户名（只能由字母，数字和下划线组成，长度2-16字符） |
| password | string | 新用户的密码SHA256值 |

**响应：** json对象，具体格式为：
```json
{
    "code": 0
}
```
| 名称 | 类型 | 描述 |
| - | - | - |
| code | int | 响应码（0 - 注册成功；1 - 用户名不符合规范；2 - 用户已存在；-1 - 未知错误）|

## 用户登录

**接口：** `[POST] /user/login`

**请求：** json对象，具体格式为：
```json
{
    "username": "xxx",
    "password": "xxx"
}
```
| 名称 | 类型 | 描述 |
| - | - | - |
| username | string | 用户名 |
| password | string | 密码SHA256值 |

**响应：** json对象，具体格式为：
```json
{
    "code": 0,
    "session": "xxx"
}
```
| 名称 | 类型 | 描述 |
| - | - | - |
| code | int | 响应码（0 - 登录成功；1 - 密码错误；2 - 用户不存在；-1 - 未知错误） |
| session | string | 用户的Session ID |

## 用户退出登录

**接口：** `[POST] /user/logout`

**请求：** json对象，具体格式为：
```json
{
    "session": "xxx"
}
```
| 名称 | 类型 | 描述 |
| - | - | - |
| session | string | 用户的Session ID |

**响应：** json对象，具体格式为：
```json
{
    "code": 0
}
```
| 名称 | 类型 | 描述 |
| - | - | - |
| code | int | 响应码（0 - 退出登录成功；-1 - 未知错误） |

## 列出所有项目

**接口：** `[POST] /user/list-projects`

**请求：** json对象，具体格式为：
```json
{
  "session": "xxx"
}
```
| 名称 | 类型 | 描述 |
| - | - | - |
| session | string | 用户的Session ID |

**响应：** json对象，具体格式为：
```json
{
  "code": 0,
  "projects": [
    "xxx",
    "yyy",
    "zzz"
  ]
}
```
| 名称 | 类型 | 描述 |
| - | - | - |
| code | int | 响应码（0 - 获取成功；1 - session无效；-1 - 未知错误） |
| projects | list | 所有项目名称的列表 |

## 创建项目

**接口：** `[POST] /user/new-project`

**请求：** json对象，具体格式为：
```json
{
  "session": "xxx",
  "name": "xxx"
}
```
| 名称 | 类型 | 描述 |
| - | - | - |
| session | string | 用户的Session ID |
| name | string | 新项目名称（长度1-256字符，只能由字母，数字和下划线组成） |

**响应：** json对象，具体格式为：
```json
{
  "code": 0
}
```
| 名称 | 类型 | 描述 |
| - | - | - |
| code | int | 响应码（0 - 获取成功；1 - session无效；2 - 项目名不符合规范；3 - 项目已存在；-1 - 未知错误） |

## 删除项目

**接口：** `[POST] /user/delete-project`

**请求：** json对象，具体格式为：
```json
{
  "session": "xxx",
  "name": "xxx"
}
```
| 名称 | 类型 | 描述 |
| - | - | - |
| session | string | 用户的Session ID |
| name | string | 要删除的项目名称 |

**响应：** json对象，具体格式为：
```json
{
  "code": 0
}
```
| 名称 | 类型 | 描述 |
| - | - | - |
| code | int | 响应码（0 - 获取成功；1 - session无效；2 - 项目不存在；-1 - 未知错误） |

## 列出所有文件

**接口：** `[POST] /project/list-files`

**请求：** json对象，具体格式为：
```json
{
  "session": "xxx",
  "project": "xxx"
}
```
| 名称 | 类型 | 描述 |
| - | - | - |
| session | string | 用户的Session ID |
| project | string | 要列出所有文件的项目名称 |

**响应：** json对象，具体格式为：
```json
{
  "code": 0,
  "files": [
    {
      "folder": 0,
      "name": "a"
    },
    {
      "folder": 1,
      "name": "b",
      "files": [
        {
          "folder": 0,
          "name": "c"
        }
      ]
    }
  ]
}
```
| 名称 | 类型 | 描述 |
| - | - | - |
| code | int | 响应码（0 - 获取成功；1 - session无效；2 - 项目不存在；-1：未知错误） |
| files | list | 包含项目根目录下所有文件和文件夹的列表。每个文件含有的字段见下表 |

每个文件含有的字段：
| 名称 | 类型 | 描述 |
| - | - | - |
| folder | int | 1代表该文件是文件夹，0代表该文件不是文件夹 |
| name | string | 文件名 |
| files | list | 若本文件是文件夹，该字段为包含其下所有文件和文件夹的列表。否则，无本字段。 |

## 创建文件

**接口：** `[POST] /project/new-file`

**请求：** json对象，具体格式为：
```json
{
  "session": "xxx",
  "project": "xxx",
  "name": "xxx"
}
```
| 名称 | 类型 | 描述 |
| - | - | - |
| session | string | 用户的Session ID |
| project | string | 项目名称 |
| name | string | 要创建的文件绝对路径 |

**响应：** json对象，具体格式为：
```json
{
  "code": 0
}
```
| 名称 | 类型 | 描述 |
| - | - | - |
| code | int | 响应码（0 - 创建成功；1 - session无效；2 - 项目不存在；3 - 文件名不符合规范；4 - 文件已存在；-1 - 未知错误） |

## 删除文件

**接口：** `[POST] /project/delete-file`

**请求：** json对象，具体格式为：
```json
{
  "session": "xxx",
  "project": "xxx",
  "name": "xxx"
}
```
| 名称 | 类型 | 描述 |
| - | - | - |
| session | string | 用户的Session ID |
| project | string | 项目名称 |
| name | string | 要删除的文件绝对路径 |

**响应：** json对象，具体格式为：
```json
{
  "code": 0
}
```
| 名称 | 类型 | 描述 |
| - | - | - |
| code | int | 响应码（0 - 删除成功；1 - session无效；2 - 项目不存在；3 - 文件不存在；4 - 路径为文件夹而非文件；-1 - 未知错误） |

## 创建文件夹

**接口：** `[POST] /project/new-folder`

**请求：** json对象，具体格式为：
```json
{
  "session": "xxx",
  "project": "xxx",
  "name": "xxx"
}
```
| 名称 | 类型 | 描述 |
| - | - | - |
| session | string | 用户的Session ID |
| project | string | 项目名称 |
| name | string | 要创建的文件夹绝对路径 |

**响应：** json对象，具体格式为：
```json
{
  "code": 0
}
```
| 名称 | 类型 | 描述 |
| - | - | - |
| code | int | 响应码（0 - 创建成功；1 - session无效；2 - 项目不存在；3 - 文件夹名不符合规范；4 - 文件夹已存在；-1 - 未知错误） |

## 删除文件夹

**接口：** `[POST] /project/delete-folder`

**请求：** json对象，具体格式为：
```json
{
  "session": "xxx",
  "project": "xxx",
  "name": "xxx"
}
```
| 名称 | 类型 | 描述 |
| - | - | - |
| session | string | 用户的Session ID |
| project | string | 项目名称 |
| name | string | 要删除的文件夹绝对路径 |

**响应：** json对象，具体格式为：
```json
{
  "code": 0
}
```
| 名称 | 类型 | 描述 |
| - | - | - |
| code | int | 响应码（0 - 删除成功；1 - session无效；2 - 项目不存在；3 - 文件夹不存在；4 - 路径为文件而非文件夹；-1 - 未知错误） |

## 上传文件
**接口：** `[POST] /project/upload-file`

**请求：** json对象，具体格式为：
```json
{
  "session": "xxx",
  "project": "xxx",
  "name": "xxx",
  "file": "xxx"
}
```
| 名称 | 类型 | 描述 |
| - | - | - |
| session | string | 用户的Session ID |
| project | string | 项目名称 |
| name | string | 要上传的文件绝对路径 |
| file | string | 要上传的文件Base64编码 |

**响应：** json对象，具体格式为：
```json
{
  "code": 0
}
```
| 名称 | 类型 | 描述 |
| - | - | - |
| code | int | 响应码（0 - 上传成功；1 - session无效；2 - 项目不存在；3 - 文件名不符合规范；4 - 路径为文件夹而非文件；5 - Base64编码无效；-1 - 未知错误） |

## 下载文件

**接口：** `[POST] /project/download-file`

**请求：** json对象，具体格式为：
```json
{
  "session": "xxx",
  "project": "xxx",
  "name": "xxx"
}
```
| 名称 | 类型 | 描述 |
| - | - | - |
| session | string | 用户的Session ID |
| project | string | 项目名称 |
| name | string | 要下载的文件绝对路径 |

**响应：** json对象，具体格式为：
```json
{
  "code": 0,
  "file": "xxx"
}
```
| 名称 | 类型 | 描述 |
| - | - | - |
| code | int | 响应码（0 - 上传成功；1 - session无效；2 - 项目不存在；3 - 文件不存在；4 - 路径为文件夹而非文件；-1 - 未知错误） |
| file | string | 要下载的文件的Base64编码 |

## 请求所有用户名下的所有项目

**接口：** `[POST] /user/get-all-project`

**请求：** 无额外请求参数

**响应：** json对象，具体格式为：
```json
{
    "code": 0,
    "projects": [
      {
        "projectUsername": "xxx",
        "projectName": "xxx",
        "projectCreateDate": "xxx",
        "projectDirectory": "xxx"
      }
    ]
}
```
| 名称 | 类型 | 描述 |
| - | - | - |
| code | int | 响应码（0 - 注册成功）|
| projects | list | 每个元素为一个项目 |
| projects[x].projectUsername | string | 拥有项目的用户名 |
| projects[x].projectName | string | 项目名 |
| projects[x].projectCreateDate | string | 项目创建时间戳（单位为ms） |
| projects[x].projectDirectory | string | 项目根目录绝对路径 |

## 请求项目日志

**接口：** `[POST] /project/log`

**请求：** json对象，具体格式为：
```json
{
  "username": "xxx",
  "projectname": "xxx"
}
```
| 名称 | 类型 | 描述 |
| - | - | - |
| code | int | 用户名 |
| projectname | string | 请求日志的项目名称 |

**响应：** json对象，具体格式为：（待补充！！）
```json
{
  "code": 0,
  "log": [
    {
      "code": "xxx",
      "time": "xxx",
      "extra_data": "xxx"
    },
  ]
}
```
| 名称 | 类型 | 描述 |
| - | - | - |
| code | int | 响应码（0 - 请求成功；1 - 用户名不存在；2 - 项目不存在；-1 - 未知错误） |
| log | list | 每个元素为一条日志 |
| log[x].code | int | 表示操作类型（0-建立项目；1-新建文件；2-新建文件夹；3-移除文件；4-移除文件夹；5-上传文件；6-下载文件；7-运行；8-调试；9-添加依赖；10-移除依赖；11-打包） |
| log[x].time | datetime | 日志生成的时间 |
| log[x].extra_data | string | 日志提供的额外信息（文件名等） |