import requests

def vreme():
	url = "https://api.open-meteo.com/v1/forecast?latitude=44.4323&longitude=26.1063&current=temperature_2m,wind_speed_10m,precipitation&timezone=auto"

	try:
		raspuns = requests.get(url)
		date = raspuns.json()

		temperatura = date["current"]["temperature_2m"]
		vant = date["current"]["wind_speed_10m"]
		precipitatii = date["current"]["precipitation"]

		print("\n --- Vremea actuala in Bucuresti ---")
		print(f"Temperatura actuala: {temperatura}°C")
		print(f"Viteza vantului: {vant} km/h")
		print(f"Precipitatii: {precipitatii} mm")
	except Exception as e:
		print(f"Eroare la prelucrarea datelor: {e}")

if __name__ == "__main__":
	vreme()
