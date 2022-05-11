# controlusoHPC

## Config

File: "service.config"

```
[config]
HOST=
PORT=
INDEX=
UC_CONVERSION=1/0
SECRET="random key"
```

## Notes


```
GET /<index_name>/_search
{
  "query": {
    "range":{
        "RecordTime":{
          "gte": 1646262000
        }
    }
  }
}
```
