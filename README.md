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


## Develop

```
export FLASK_APP=apicontrolusohpc
export FLASK_ENV=development
flask run
# flask run --host 0.0.0.0
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
