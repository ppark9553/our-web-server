from gateway.controllers import gateway_reducer

@gateway_reducer
def test_action(**params):
    task_1 = params['task_1']
    testing_words = params['testing_words']

    print('running gobble.tasks.test_action function')
    print(testing_words)
    task_1()
