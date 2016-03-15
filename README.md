# CapptainUtilities

Python scripts to interact with [app.capptain.com](https://app.capptain.com/) REST APIs.

## Interacting with [Segments API](https://app.capptain.com/doc/SaaS/Segments%20API/index.html)

### List 5 segments

`python capptain.py --appid <app id> --apikey <app key> --api segments --limit 5`

### Store given application segments

Segments will be stored to `data/<app id>/segments/list.json`

`python capptain.py --appid <app id> --apikey <app key> --api segments --cmd liststore`
  
### Store given application segments

Segment will be stored to  `data/<app id>/segments/segment_<segment id>.json`


`python capptain.py --appid <app id> --apikey <app key> --api segments --cmd segment --id <segment id>`

### Create a segment from a template json defining the criteria
  
`python capptain.py --appid <app id> --apikey <app key> --api segments --cmd segmentcreate --definition <path to template json>` 

Here is a sample json
```
{
  "criteria": [
    {
      "criterionName": "MyCriteriaName", 
      "extra": {
        "key": "MyApplicationErrorExtraName", 
        "operator": "EQ", 
        "value": "802"
      }, 
      "name": "MyApplicationError", 
      "occurrence": {
        "operator": "GE", 
        "period": "total", 
        "value": 1
      }, 
      "period": {
        "predefined": "current-week", 
        "type": "predefined"
      }, 
      "type": "error"
    }
  ], 
  "name": "MySegmentName"
}
```

### Operate on many applications at a time

One need to list the applications in a JSON file like
```
{
  "apps": [
    {
      "name": "app_a", 
      "appid": "<app_a id>", 
      "apikey": "<app_a apikey>",
      "monitorapikey": "<app_a monitoringapikey>"
    },
    {
      "name": "app_b", 
      "appid": "<app_b id>", 
      "apikey": "<app_b apikey>",
      "monitorapikey": "<app_b monitoringapikey>"
    },
    {
      "name": "app_c", 
      "appid": "<app_c id>", 
      "apikey": "<app_c apikey>",
      "monitorapikey": "<app_c monitoringapikey>"
    }
  ]
}
```

Finally appid and apikey arguments are replaced by the appregistry argument.
appregistry references the application registry json file.

`python capptain.py --appregistry myappregistry.json --api segments --limit 5`

A subset of the registry can be addressed by specifying the apps argument:

`python capptain.py --appregistry --apps "app_a;app_c" myappregistry.json --api segments --limit 5`
