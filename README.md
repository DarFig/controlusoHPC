# controlusoHPC

## Config

File: "service.config"

```
[config]
HOST=
PORT=
INDEX=
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
