
def choose_from_list(choice_list):
    """
    Prompts user to choose a values from a list, returning that value as the output.
    ***
    ARGS
    choice_list: list, list of values to choose from
    ***
    """
    choices = dict(enumerate(choice_list))
    display = '\n'.join(["[%d] %s"%(k,v) for
                        k,v in choices.items()])
    print(display)
    n = input("Choose one of %s"%', '.join([str(k) 
              for k in choices.keys()]))
    choice = choices[int(n)]
    print("\nSelected: %s"%choice)
    return choice
