# Gecode_address_restful-API

# API Documention:
path the address as parameter to the API http://localhost:8080/home/Tokyo,%20Japan
later we will add paramter for your api id to test you gecode API calls like curl  and postman, it will handle alot API

# what is it
Using google geocoding to build UI restful API receive address call geocoding API get result store in database, in case of error create new error recorded in Request Error table it return name, geocode, city id , with AI logic if users searched all the address exist my app will have the all data in google Geocode API  and can handle it self without calls, also to reduice API calls, you can query dp if there is that address return from db not make new api call
