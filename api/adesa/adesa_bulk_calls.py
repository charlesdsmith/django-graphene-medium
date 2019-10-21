import requests
import json

test = ['VHSRLAFKStest', 'No Issues Reported', 'No Issues Reported', 'No Issues Reported', 'No Issues Indicated', 'No Issues Reported', 'some Recalls Reported', '12-01-2018']
# MAKE SURE TO USE "application/json" IN "Content-Type"


def authorize():

    client_id = 'SF4ndlds1e6H5cAAi8vpxDzQB0zbkslfqiH1CgXb'
    client_secret = 'vznY2auvuqGnTKdaYOA6tqlpASRXU6dEe6V3ZdZblX2RVvQGdh2c1IF6byVpxOafdfqbysthAxeXkTyMI7R5SExvK6MbDEhXaaF4YXg9Wz9GyCXIZ97eCf6VaH8MlTEO'

    local_client_id = '8TqPw5f2WgdNiY8qFZ97oh7wDQhVNnuuKyJ30dUd'
    local_client_secret = 'F2MCmGC3EapJBWH7c446qpsQpj0fxYde9MKRXL8CsH514uN1CbMh654WrT8ZqqfrsZnsitsNnI4MeZEzmZu4t2at7ViEWDbELKzqUHeJWevyrpoeInSoJpEARxYvPs9R'

    data = {
        'grant_type': 'password',
        'username': 'charles',
        'password': 'charles',
    }


    #heroku_response = requests.post('https://gsm-django.herokuapp.com/o/token/', data=data, auth=(client_id, client_secret))
    response = requests.post('http://127.0.0.1:3000/o/token/', data=data, auth=(local_client_id, local_client_secret))

    return response.text

def bulk_post():
    # create multiple resources
    # [{"field":"value","field2":"value2"}]

    headers = {
        'Content-Type': "application/json",
        'Authorization': 'Bearer Lvh03et4eQuVE3QjxLrcXvjxjQDORZ',
    }

    data = [{
        "vin": "123456",
        "img_url": "https://germanstarmotors.slack.com/messages/DE33RNUSHTEST2/",
        "year": "1991",
        "grade": "4",
        "run_date": "11-28-2018",
        "lane": "2"
        },
        {
        "vin": "654321",
        "img_url": "https://germanstarmotors.slack.com/messages/DE33RNUSHTEST3/",
        "year": "1991",
        "grade": "5",
        "run_date": "11-29-2018",
        "lane": "3"}
        ]

    data = json.dumps(data)
    # response = requests.post('http://gsm-dango.herokuapp.com/api/v1/carfax/', headers=headers, cookies=cookies, data=data)

    try:
        #heroku_response = requests.post('https://gsm-django.herokuapp.com/api/v1/adesa_run_list_bulk_upload/', data=data, headers=headers)
        response = requests.post('http://127.0.0.1:3000/api/v1/adesa_run_list_bulk_upload/', data=data, headers=headers)
        # print(json.dumps(response.json))
        #print(heroku_response.status_code)
        return response.text
    except Exception as e:

        print(e)

if __name__ == "__main__":
    print(authorize())
    #print(post_run_list())
    #print(bulk_post())
