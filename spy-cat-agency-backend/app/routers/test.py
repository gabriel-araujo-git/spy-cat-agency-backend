import requests

url = "https://api.thecatapi.com/v1/breeds"
response = requests.get(url)
breeds = response.json()

breed_names = [breed["name"] for breed in breeds]

print(breed_names)
