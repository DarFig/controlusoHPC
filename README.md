# controlusoHPC



### Notes


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
