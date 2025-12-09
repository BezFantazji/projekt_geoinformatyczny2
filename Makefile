run:
	docker build -t air-dashboard .
	docker run -p 8000:8000 air-dashboard
