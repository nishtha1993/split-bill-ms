def parse_group_item(item):
    """
    Group item from dynamo is like this

    {
    'groupId': {
      'S': '95e7cc69-e932-42d6-97b5-175e58f74a51'
    },
    'members': {
      'L': [
        {
          'S': 'abc@xyz.com'
        }
      ]
    },
    'name': {
      'S': 'test'
    }
  }
    needs to be converted correctly
    """
    result = {
        "groupId": list(item["groupId"].values())[0],
        "name": list(item["name"].values())[0],
        "members": []
    }

    if "imageS3Link" in item:
        result["imageS3Link"] = list(item["imageS3Link"].values())[0]

    for memberEmail in item["members"]["L"]:
        email = memberEmail["S"]
        result["members"].append(email)

    return result
