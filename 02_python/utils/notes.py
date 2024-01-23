command_name, options, positional_args = '', [], []
input_command = "cp -i -v qwe.py commands"
input_command = input_command.split(" ")
command_name = input_command[0]

for i in input_command[1:]:
    if '-' in i:
        options.append(i)
    else:
        positional_args.append(i)
        
result = {'command_name': command_name,'options': options,'args': positional_args}
print(result)
