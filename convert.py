class Number_system:
    """
        converts value of Number System from baseX to baseY provided baseX, baseY is >=2 and <= 36         
    """
    def __init__(self):
        # accepted number range from, 0 - Z
        self.legal_base_36 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def base_validator(self, base):
        '''
            checks if base is acceptable, >= 2 and <= 36
        '''
        return True if base.isdigit() and 1 < int(base) <= 36 else False

    def inp_validator(self, value):
        '''
            checks if input number system is within acceptable base range[0-9A-Z]
        '''
        return True if set( value ) .issubset( self.legal_base_36 ) else False

    def validate(self, value, base):
        '''
            checks if the condition for coverting Number system from 
            baseX to baseY is satisfied
        '''
        if  not self.inp_validator(value):
            return Exception("Invalid Number System")

        if not self.base_validator(base):
            return Exception("Base must be an integeral value within range of 2 and 36 inclusive")

        else:
            min_base =  self.legal_base_36.rfind(max(value))
            return Exception(f"Invalid base for '{value}'") if min_base >= int(base) else True

    def baseX_to_base10(self, value, base):
    
        '''
            Converts number system from any base  provided 
            base is >=2 and <=36 to equivalent value in base10
        '''
        value_in_base10 = 0

        if type(check := self.validate(value, base)) is not Exception:
            operand = [ x for x in value]  # stores a list of value i.e "1A2Z" = ['1','A','2','Z']
            
            for index, num in enumerate(operand[::-1]):
                if num.isalpha():
                    num = self.legal_base_36.rfind(num) # i.e A, Z turns to 10, 35 repectively
                value_in_base10 += (int(num) * int(base)**index)
            return value_in_base10
        return check

    def base10_to_baseX(self, value, baseX):
    
        '''
            Converts number system originally in base10 to
            equivalent value in baseX provided baseX >=2 and <= 36
        '''
        value_to_baseX = ""
        value, baseX =  int(value), int(baseX)

        if baseX == 10 or value == 0:
            return str(value)

        if value < 0: # checks if value is a negative value 
            value = abs(value) # turn to positive value  using abs()
            value_to_baseX += "i"  # makes the result into a complex number to indicate its a negative value

        while value > 0:
            rem = divmod(value,baseX)
            value_to_baseX += str(rem[1]) if rem[1] <=9 else self.legal_base_36[rem[1]].upper()
            value = rem[0]
    
        return value_to_baseX[::-1]