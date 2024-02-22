import FlightRadar24
from FlightRadar24 import FlightRadar24API
import datetime
import time
from datetime import timedelta

class RealTimeParser:
    def get_string_flight_info(self, flight: FlightRadar24.Flight) -> str:
        time_now = datetime.datetime.now().strftime("%H:%M:%S")
        return f"{flight.callsign} {datetime.datetime.now().date()} {time_now} {flight.latitude:.6f} {flight.longitude:.6f} {flight.altitude} {flight.ground_speed}"

    def get_string_callsign_info(self, flight: FlightRadar24.Flight) -> str:
        time_now = datetime.datetime.now().strftime("%H:%M:%S")
        return f"{flight.callsign} {flight.aircraft_code} {datetime.datetime.now().date()} {time_now}"

    def logSheremetyegoFlights(self, hours: int, minutes: int, seconds: int):
        sheremetyevo_cords = (55.973233, 37.409741)
        update_frequency = 5
        save_file = "sheremetyevo_history"
        callsigns_file = "callsign_info"
        fr_api = FlightRadar24API()
        all_callsigns: dict = {}
        time_to_stop = datetime.datetime.now() + timedelta(hours=float(hours), minutes=float(minutes), seconds=float(seconds))

        with open(save_file, "a") as s_file:
            with open(callsigns_file, "a") as c_file:
                while datetime.datetime.now() < time_to_stop:
                    flights = fr_api.get_flights(
                        bounds=fr_api.get_bounds_by_point(sheremetyevo_cords[0], sheremetyevo_cords[1], 20000))
                    for flight in flights:
                        s_file.write(self.get_string_flight_info(flight))
                        s_file.write('\n')

                        if str(flight.callsign) not in all_callsigns:
                            c_file.write(self.get_string_callsign_info(flight))
                            c_file.write('\n')
                            all_callsigns[str(flight.callsign)] = 1
                    time.sleep(update_frequency)