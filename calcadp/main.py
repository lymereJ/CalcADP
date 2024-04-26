import logging
from CoolProp.HumidAirProp import HAPropsSI
from CoolProp.HumidAirProp import HAPropsSI


class Calc:
    def __init__(self, barometric_pressure, tolerance):
        self.tolerance = tolerance
        self.pressure = barometric_pressure

    def apparatus_dew_point(self, w_in, w_out, t_in, t_out):
        """Determine aparatus dew point corresponding to the temperature and humidity ratio of two distinct point on the humid air psychrometric chart

        :parm float w_in: Humidity ratio of the first point
        :parm float w_out: Humidity ratio of the second point
        :parm float t_in: Dry-bulb temperature of the first point in degree Celsuis
        :parm float t_out: Dry-bulb temperature of the second point in degree Celsuis
        :return: Aparatus dew point in degree Celsuis
        :rtype: float

        """
        # TODO: Input validation
        # Define relationship between temperatures and humidity ratios
        # for the two reference points
        # w_x = a * t_x + b
        a = (w_out - w_in) / (t_out - t_in)
        b = w_in - a * t_in

        # Initialization
        t_adp = t_out
        incr = 0.001
        t_x = t_out + incr
        found_solution = False

        # Iterate to find ADP
        while not found_solution:
            # Reinitialization
            t_x += incr
            w_x = a * t_x + b

            # Calculate ADP
            t_adp = (
                HAPropsSI("D", "T", t_x + 273.15, "P", self.pressure, "W", w_x) - 273.15
            )

            # Check if a solution has been found
            if abs(t_adp - t_x) < self.tolerance:
                found_solution = True

            # Reduce increment as we approach a solution
            incr = (t_adp - t_x) / 10
        return t_adp
