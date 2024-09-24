from pc2repka_console import Action, change_args_type, local_except


class right(Action):
    '''  right <dist> <vel> - Moving right on distance with specified velocity'''
    @change_args_type
    def execute(self):
        try:
            dist, vel = self.args 
            device = self.device
            device.publish(f"Moving {dist}m right with {vel} m/s")
        except:
            print("Not enough arguments, there must be 2")
            raise local_except()
        print(f"Moving {dist}m right with {vel} m/s")

    