from retroactive import FullRetroactivePriorityQueue, PartialRetroactivePriorityQueue, \
    Query, InsertOperations, Operations


class UserInterface:

    @classmethod
    def get_type_class(cls):
        options = {'1': FullRetroactivePriorityQueue, '2': PartialRetroactivePriorityQueue}
        print("Choose Type of retroactive data structure and enter the matched number:"
              "\nFull Retroactive: 1"
              "\nPartial Retroactive: 2")
        while True:
            full_partial = input("Type: ").strip()
            if full_partial in options:
                return options[full_partial]
            else:
                print('INVALID INPUT')

    @classmethod
    def get_retroactive_operation(cls, retroactive_obj):
        options = {1: {'method': retroactive_obj.insert,
                       'args': {'operation': {'method': cls.get_insert_operation, 'condition': True, 'value': None},
                                'time': {'method': cls.get_time, 'condition': True, 'value': None},
                                'value': {'method': cls.get_value, 'condition': False, 'value': None}}},
                   2: {'method': retroactive_obj.delete,
                       'args': {'time': {'method': cls.get_time, 'condition': True, 'value': None}}},
                   3: {'method': retroactive_obj.query,
                       'args': {'query': {'method': cls.get_query_operation, 'condition': True, 'value': None},
                                'time': {'method': cls.get_time,
                                         'condition': retroactive_obj.__class__ == FullRetroactivePriorityQueue,
                                         'value': None}}}}
        print("Choose Retroactive Operation and enter the matched number")
        for opt_name, opt_value in Operations.get_dict().items():
            print(f"{opt_name}: {opt_value}")
        while True:
            user_input = input('Operation: ').strip()
            try:
                user_input = int(user_input)
                if user_input in options.keys():
                    args = updated_args = options[user_input]['args']
                    kwargs = dict()
                    for arg_name, arg_data in args.items():
                        updated_args = cls.update_conditions(updated_args)
                        if updated_args[arg_name]['condition']:
                            kwargs[arg_name] = updated_args[arg_name]['value'] = arg_data['method']()
                    return options[user_input]['method'], kwargs
                else:
                    print('INVALID INPUT')
            except ValueError:
                print('INVALID INPUT')

    @classmethod
    def update_conditions(cls, args: dict):
        """
        this function is for pop operation in insert
        :param args:
        :return:
        """
        if 'operation' in args and args['operation']['value'] is not None:
            args['value']['condition'] = args['operation']['value'] == InsertOperations.Push
        return args

    @classmethod
    def get_insert_operation(cls):
        print("Choose Insert Operation and enter the matched number")
        for opt_name, opt_value in InsertOperations.get_dict().items():
            print(f"{opt_name}: {opt_value}")
        while True:
            user_input = input('Insert Operation: ').strip()
            try:
                user_input = int(user_input)
                if user_input in InsertOperations.get_inverse_dict():
                    return InsertOperations.get_inverse_dict()[user_input]
                else:
                    print('INVALID INPUT')
            except :
                print('INVALID INPUT')

    @classmethod
    def get_query_operation(cls):
        print("Choose Query Type and enter the matched number")
        for opt_name, opt_value in Query.get_dict().items():
            print(f"{opt_name}: {opt_value}")
        while True:
            user_input = input('Query Type: ').strip()
            try:
                user_input = int(user_input)
                if user_input in Query.get_inverse_dict():
                    return Query.get_inverse_dict()[user_input]
                else:
                    print('INVALID INPUT')
            except:
                print('INVALID INPUT')

    @classmethod
    def get_time(cls):
        print("please enter the time that operation happens")
        while True:
            user_input = input('Time: ').strip()
            try:
                user_input = int(user_input)
                return user_input
            except:
                print('INVALID INPUT')

    @classmethod
    def get_value(cls):
        print("please enter the value that you want to push to queue ")
        while True:
            user_input = input('Value: ').strip()
            try:
                user_input = int(user_input)
                return user_input
            except:
                print('INVALID INPUT')

    @classmethod
    def run(cls):
        try:
            retroactive_class = cls.get_type_class()
            retroactive_obj = retroactive_class()
            while True:
                    function, kwargs = cls.get_retroactive_operation(retroactive_obj)
                    result = function(**kwargs)
                    if result:
                        print(result)
                    else:
                        retroactive_obj.print()
        except:
            pass


if __name__ == "__main__":
    UserInterface.run()