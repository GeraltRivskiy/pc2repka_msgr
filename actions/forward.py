from pc2repka_console import Action, change_args_type, local_except


class forward(Action):
    '''  forward <dist> <vel> - Moving forward on distance with specified velocity'''
    @change_args_type
    def execute(self):
        try:
            dist, vel = self.args 
            device = self.device
            device.publish(f"Moving {dist}m forward with {vel} m/s")
        except:
            print("Not enough arguments, there must be 2")
            raise local_except()
        print(f"Moving {dist}m forward with {vel} m/s")

    