# make calls to /graphql here

import json
import requests

def get_graphql(query):

    response = requests.get('http://localhost:3000/graphql?query=%s' % query)
    return response.text


def post_graphql(query=None):

    headers = {
        'Authorization': 'Bearer jAL8mDIwpm7Pqk7BUtelsgW3jIFUkO',
        "Content-Type": "application/json",

    }

    data = {
        "query": """ {
  allBids{
    bid_id
    amount
  }
  
}""",
        }

    data1 = {
        "query": """mutation update($vin:String!, $runDate:String!, $humanValuation:String!){
  updateShoppinglist(lookupFields: {vin:$vin, runDate:$runDate}, fieldsToUpdate:{ humanValuation: $humanValuation}){
    runlist{
      vin
      runDate
      humanValuation
         }
         }
        }""",
        "variables": {"vin": "123456", "runDate": "11-28-2018", "humanValuation": "234"},
    }

    data1 = json.dumps(data1)
    data = json.dumps(data)

    response = requests.post("http://localhost:3000/graphql", headers=headers, data=data1)
    #response2 = requests.post("https://gsmauctionapp.herokuapp.com/graphql/", headers=headers, data=data)
    #print(response.text)

    #print(response.status_code)
    print(response.content)
    return response

if __name__ == "__main__":

    post_graphql()

    '''print(get_graphql("""query getCarFaxByRundate {
  carfax(runDate:"11-18-2018"){
    vin
  }
}"""))'''


