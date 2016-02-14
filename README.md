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
