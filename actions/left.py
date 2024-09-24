from pc2repka_console import Action, change_args_type, local_except


class left(Action):
    '''  left <dist> <vel> - Moving left on distance with specified velocity'''
    @change_args_type
    def execute(self):
        try:
            dist, vel = self.args 
            device = self.device
            device.publish(f"Moving {dist}m left with {vel} m/s")
        except:
            print("Not enough arguments, there must be 2")
            raise local_except()
        print(f"Moving {dist}m left with {vel} m/s")

    